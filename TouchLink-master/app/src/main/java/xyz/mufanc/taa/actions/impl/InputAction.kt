package xyz.mufanc.taa.actions.impl

import xyz.mufanc.taa.actions.IAction
import xyz.mufanc.taa.input.InputDispatcher
import xyz.mufanc.taa.input.InputEvent

class InputAction : IAction {

    var inputs: List<InputEvent> = emptyList()

    override fun run(): String {
        return InputDispatcher.dispatchInputs(inputs)
    }
}
