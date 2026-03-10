package xyz.mufanc.taa.misc

import android.util.Log

object Log {

    private const val TAG = "TouchLink"

    fun d(tag: String, message: String) {
        Log.d(TAG, ("[$tag] $message"))
    }

    fun e(tag: String, message: String, err: Throwable) {
        Log.e(TAG, "[$tag] $message\n${Log.getStackTraceString(err)}")
    }
}
