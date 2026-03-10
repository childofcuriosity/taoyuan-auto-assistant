package xyz.mufanc.taa.actions.impl

import xyz.mufanc.taa.actions.ActionResult
import xyz.mufanc.taa.actions.IAction
import xyz.mufanc.taa.actions.ISuperAction
import xyz.mufanc.taa.misc.JsonCompat

class TouchLinkAction(
    val action: String,
    val params: Map<String, Any>
) : ISuperAction {

    override fun run(): String {
        val action = downcast() ?: return ActionResult.failed("unknown action")
        return action.run()
    }

    override fun downcast(): IAction? {
        return when (action) {
            "input" -> JsonCompat.fromJsonValue<InputAction>(params)
            else -> null
        }
    }
}
