package xyz.mufanc.taa.input

import android.graphics.Point
import java.io.Serializable

class InputEvent : Serializable {

    var action: String? = null
    var delay: Long = 0
    var duration: Long = 0
    var args: List<Int> = emptyList()
    var extras: Map<String, Int> = emptyMap()

    fun downcast(): Action? {
        return when (action) {
            "touch" if args.size == 2 -> {
                Action.Touch(Point(args[0], args[1]), delay, duration)
            }
            "swipe" if args.size >= 2 && args.size % 2 == 0 -> {
                val points = ArrayList<Point>(args.size / 2)

                for (i in args.indices step 2) {
                    points.add(Point(args[i], args[i + 1]))
                }

                Action.Swipe(points, extras["stabilize"]?.toLong() ?: 0)
            }
            else -> null
        }
    }

    override fun toString(): String {
        return "InputEvent[action=$action|delay=$delay|duration=$duration|args=$args]"
    }

    sealed class Action {

        abstract val delay: Long
        abstract val duration: Long

        data class Touch(
            val point: Point,
            override val delay: Long = 0,
            override val duration: Long = 0
        ) : Action()

        data class Swipe(
            val points: List<Point>,
            val stabilize: Long,
            override val delay: Long = 0,
            override val duration: Long = 0
        ) : Action()
    }
}
