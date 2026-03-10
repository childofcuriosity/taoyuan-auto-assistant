package xyz.mufanc.taa

import xyz.mufanc.taa.actions.ActionResult
import xyz.mufanc.taa.actions.impl.TouchLinkAction
import xyz.mufanc.taa.misc.JsonCompat
import xyz.mufanc.taa.misc.Log
import java.io.BufferedReader
import java.io.InputStreamReader

object Main {

    private const val TAG = "Main"

    @JvmStatic
    fun main(args: Array<String>) {
        Thread.setDefaultUncaughtExceptionHandler { th, err ->
            Log.e(TAG, "Uncaught exception on thread: $th", err)
        }

        val reader = BufferedReader(InputStreamReader(System.`in`))

        while (true) {
            val line = reader.readLine() ?: break

            if (line.isBlank()) {
                continue
            }

            try {
                val action: TouchLinkAction? = JsonCompat.fromJson(line.trim())

                if (action == null) {
                    println(ActionResult.failed("failed to parse command"))
                    continue
                }

                println(action.run())
            } catch (err: Throwable) {
                Log.e(TAG, "unknown error", err)
                println(ActionResult.failed(err.message))
            }
        }
    }
}
