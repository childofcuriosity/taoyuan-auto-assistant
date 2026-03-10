package xyz.mufanc.taa.actions

interface ISuperAction : IAction {
    fun downcast(): IAction?
}
