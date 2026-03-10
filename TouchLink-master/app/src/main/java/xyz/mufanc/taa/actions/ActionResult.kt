package xyz.mufanc.taa.actions

import xyz.mufanc.taa.misc.JsonCompat
import java.io.Serializable

data class ActionResult(
    val success: Boolean = false,
    val message: String? = null
) : Serializable {

    companion object {
        fun success(msg: String? = null): String {
            return JsonCompat.toJson(ActionResult(true, msg))!!
        }

        fun failed(msg: String? = null): String {
            return JsonCompat.toJson(ActionResult(false, msg))!!
        }
    }
}
