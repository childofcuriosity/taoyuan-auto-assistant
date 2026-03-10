package xyz.mufanc.taa.misc

import com.squareup.moshi.Moshi
import com.squareup.moshi.kotlin.reflect.KotlinJsonAdapterFactory

object JsonCompat {

    val moshi: Moshi = Moshi.Builder().add(KotlinJsonAdapterFactory()).build()

    inline fun <reified T> fromJson(json: String): T? {
        val adapter = moshi.adapter(T::class.java)
        return adapter.fromJson(json)
    }

    inline fun <reified T> fromJsonValue(value: Any?): T? {
        val adapter = moshi.adapter(T::class.java)
        return adapter.fromJsonValue(value)
    }

    inline fun <reified T> toJson(value: T): String? {
        val adapter = moshi.adapter(T::class.java)
        return adapter.toJson(value)
    }
}
