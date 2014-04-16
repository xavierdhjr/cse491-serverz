package controllers

import play.api._
import play.api.mvc._
import play.api.db._

import models.AppImage

object Application extends Controller {

  def index = Action {
    Ok(views.html.index("Your new application is ready."))
  }

  def image_raw = Action { implicit request =>
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