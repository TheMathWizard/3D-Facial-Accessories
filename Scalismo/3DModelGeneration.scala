
import scalismo.utils.Random

scalismo.initialize()
implicit val rnd = Random(1024)

import scalismo.faces.io._
import scalismo.faces.color._
import scalismo.faces.image._
import java.io.File
import scalismo.faces.gui._
import GUIBlock._

/////////////////////////////
//Parameter initialisation
/////////////////////////////
val fileName = "img7"
val imgFileAddr = "data/" + fileName + "/" + fileName + "-crop.jpg"
val rpsFileAddr = "data/" + fileName + "/" + fileName + "-rps.rps"
val meshFileAddr = "data/" + fileName + "/" + fileName + "-mesh.ply"
val texturedMeshFileAddr = "data/" + fileName + "/" + fileName + "-texture.ply"
/////////////////////////////

val targetImage = PixelImageIO.read[RGBA](new File(imgFileAddr)).get
val targetPanel = ImagePanel(targetImage, RGB.Black.toAWTColor)
val targetLabel = label("Target Image")

stack(
  targetPanel,
  targetLabel
).displayIn("Image Fitting GUI")

import java.net.URI
import scalismo.faces.io.MoMoIO
import scalismo.faces.sampling.face._
import scalismo.faces.parameters._

val momoFile = new File("data/model2017-1_face12_nomouth.h5")
val momoURI = momoFile.toURI
val momo = MoMoIO.read(momoURI).get.neutralModel
val modelRenderer = MoMoRenderer(momo)

// val init = RenderParameter.default.
//   forImageSize(targetImage.width, targetImage.height).
//   withMoMo(MoMoInstance.zero(50, 50, 0, momoURI))

val targetInit = RenderParameterIO.read(new File("data/init.rps")).get

val modelImage = modelRenderer.renderImage(targetInit)

val imagePanel = ImagePanel(modelImage, RGB.Black.toAWTColor)
val imageLabel = label("Model")

shelf(
    stack(
      targetPanel,
      targetLabel),
    stack(
      imagePanel,
      imageLabel)
).displayIn("Image Fitting GUI").pack()


import  scalismo.faces.io.RenderParameterIO

import faces.tutorial.util.Helpers._

val overlay = OverlayRenderer(modelRenderer, targetImage, imagePanel)

overlay.render(targetInit)

/////////////////////////////
//Proposal initialisation
/////////////////////////////

overlay.render(targetInit)

import scalismo.faces.sampling.face.evaluators._

val stddevForeground = 0.05
val stddevBackground = 3.0
val allPixelEval = IndependentPixelEvaluator.isotropicGaussianConstantBackground(targetImage, stddevForeground, stddevBackground)

import scalismo.faces.sampling.face.evaluators._

val imageEval = ImageRendererEvaluator(modelRenderer, allPixelEval)

import scalismo.sampling.evaluators._
import ProductEvaluator.implicits._
import scalismo.faces.sampling.face.evaluators.PriorEvaluators._

val priorShape = GaussianShapePrior(0.0, 1.0)
val priorTexture = GaussianTexturePrior(0.0, 1.0)
val prior = ProductEvaluator(priorShape, priorTexture)

val posterior = ProductEvaluator(prior * imageEval)

import scalismo.geometry._
import scalismo.sampling.proposals._
import scalismo.faces.sampling.face.proposals._
import SphericalHarmonicsLightProposals._
import ParameterProposals.implicits._
import MixtureProposal.implicits._

val yawProposal   = GaussianRotationProposal(Vector3D.unitY, degToRad(1.0))
val nickProposal  = GaussianRotationProposal(Vector3D.unitX, degToRad(1.0))
val rollProposal  = GaussianRotationProposal(Vector3D.unitZ, degToRad(1.0))
val rotationProposal = MixtureProposal(yawProposal + nickProposal + rollProposal).toParameterProposal

val translationProposal = GaussianTranslationProposal(Vector2D(5, 5)).toParameterProposal

val scalingProposal = GaussianScalingProposal(math.log(1.05)).toParameterProposal

val distanceProposal = GaussianDistanceProposal(20, compensateScaling = true)

val poseProposal = MixtureProposal(
  rotationProposal + translationProposal + scalingProposal + distanceProposal
)

val shapeProposal = GaussianMoMoShapeProposal(0.05).toParameterProposal

val colorProposal = GaussianMoMoColorProposal(0.05).toParameterProposal

val lightProposal1 = SHLightPerturbationProposal(0.001, true).toParameterProposal
val lightProposal2 = SHLightIntensityProposal(0.1).toParameterProposal
val lightProposal = MixtureProposal(lightProposal1 + lightProposal2)

val proposalDistribution = MixtureProposal(
  poseProposal +
  2 *: shapeProposal +
  2 *: colorProposal +
  2 *: lightProposal
)

import scalismo.sampling.loggers._

val valueLogger = createValueLogger(imageLabel)

val guiImageLogger = new ChainStateLogger[RenderParameter] {
  override def logState(sample: RenderParameter): Unit = overlay.render(sample)
}.subSampled(50)

import scalismo.sampling.algorithms._
import scalismo.faces.sampling.evaluators._
import CachedDistributionEvaluator.implicits._

val cachedPosterior = posterior.cached(5)

val imageSampler = MetropolisHastings(
  proposalDistribution,
  cachedPosterior
)

import scalismo.sampling.loggers.ChainStateLogger.implicits._

case class Sample(number: Int,
                  sample: RenderParameter,
                  posteriorValue: Double)

val posteriorSampleIterator = imageSampler.iterator(
  targetInit,
  valueLogger
).loggedWith(guiImageLogger)

val posteriorSamples = posteriorSampleIterator.zipWithIndex.map{
  case (sample, index) =>
    Sample(
      index,
      sample,
      cachedPosterior.logValue(sample)
    )
}.take(2000).toIndexedSeq

val bestSample = posteriorSamples.maxBy{
  case Sample(it, x, value) => value
}

val bestSample_RP = bestSample.sample
overlay.render(bestSample_RP)

RenderParameterIO.write(bestSample_RP, new File(rpsFileAddr))

/////////////////////////////
//Saving the best model as a .ply file
/////////////////////////////

val bestSampleMoMo = bestSample_RP.momo

val bestSampleMoMoInstance = bestSample_RP.momo
import scalismo.faces.parameters._
import scalismo.faces.mesh._
import java.awt.Color
import scalismo.faces.io.MeshIO
import scalismo.common._
import scalismo.geometry._
import scalismo.mesh._

val bestMesh: VertexColorMesh3D = momo.instance(bestSampleMoMoInstance.coefficients)
MeshIO.write(bestMesh, new File(meshFileAddr))

/////////////////////////////
//2D Texture Mapping
/////////////////////////////

import scala.io.Source
import java.io._

val bufferedSource = Source.fromFile(meshFileAddr)

val newFile = new File(texturedMeshFileAddr)
val bw = new BufferedWriter(new FileWriter(newFile))
var i : Int = 0

for (line <- bufferedSource.getLines) {
  
  if(i>=14 && i < 28588+14){
    val strings = line.split(" ")
    //print(strings(0) + strings(1) + strings(2) + "\n")
    val point : Point[_3D] = Point3D(strings(0).toDouble, strings(1).toDouble, strings(2).toDouble)
    val pointInImage = bestSample_RP.renderTransform(point)
    val imgcolour = targetImage(pointInImage(0).toInt, pointInImage(1).toInt).toTuple
    
    bw.write(strings(0) + " " + strings(1) + " " + strings(2) + " " + (imgcolour._1 * 255.0).toInt + " " + (imgcolour._2 * 255.0).toInt + " " + (imgcolour._3 * 255.0).toInt + " " + (imgcolour._4 * 255.0).toInt + "\n")
  }else{
    bw.write(line + "\n")
  }
  i = i + 1
}
println("Mesh written")
bw.close()
bufferedSource.close
