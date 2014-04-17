package controllers

import play.api._
import play.api.mvc._
import play.api.db._
import play.api.libs.iteratee.Enumerator
import models.AppImage
import play.api.libs.concurrent.Execution.Implicits._

object Application extends Controller {

  def index = Action {
    Ok(views.html.index("Welcome."))
  }
  def upload = Action {
    Ok(views.html.upload())
  }
  
  def get_image = Action { implicit request =>
	val imageId = request.getQueryString("id")
	val special = request.getQueryString("special")

	special match{
		case Some(s) =>
			Ok(AppImage.get_latest data).as("image/png")
		case None =>
			//BadRequest(views.html.index("Bad Request."))
			imageId match{
				case Some(id) =>
					Ok(AppImage.get_image(id.toLong) data).as("image/png")
				case None =>
					BadRequest(views.html.index("Bad Request."))
			}
	}
  }
  
  def add_image = Action(parse.multipartFormData) { request =>
	request.body.file("image").map{ image =>
		import java.io.File
		val fileName = image.filename
		val contentType = image.contentType

		val fileContent: Array[Byte] = scala.io.Source.fromFile(image.ref.file, "ISO-8859-1").map(_.toByte).toArray
		
		AppImage.add(fileContent)
		//SimpleResult(
		//	header = ResponseHeader(200, Map(CONTENT_LENGTH -> image.ref.file.length.toString)),
		//	body = "Success"
		//)
		Ok(views.html.index("Sucessfully uploaded image."))
	}.getOrElse {
		Redirect(routes.Application.index).flashing(
		  "error" -> "Missing file"
    )
  }
  }
  
  def stats = Action { implicit request =>
	val stat = request.getQueryString("stat")

	stat match{
		case Some(s) =>
			if(s == "count") Ok(AppImage.get_count.toString)
			else BadRequest(views.html.index("Bad Stat."))
		case None =>
			BadRequest(views.html.index("Bad Request."))
	}
  }
  
}