package xyz.mufanc.taa.actions

import java.io.Serializable

interface IAction : Serializable {
    fun run(): String
}
