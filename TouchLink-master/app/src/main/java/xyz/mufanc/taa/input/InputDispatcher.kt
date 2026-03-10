package xyz.mufanc.taa.input

import android.annotation.SuppressLint
import android.os.Handler
import android.os.HandlerThread
import android.os.MessageQueue
import android.os.SystemClock
import androidx.core.os.postAtTime
import androidx.core.os.postDelayed
import xyz.mufanc.taa.actions.ActionResult
import xyz.mufanc.taa.input.InputEvent.Action
import xyz.mufanc.taa.misc.Log
import kotlin.math.sqrt

object InputDispatcher {

    private const val TAG = "InputDispatcher"

    fun dispatchInputs(inputs: List<InputEvent>): String {
        val actions = inputs.map { event ->
            event.downcast() ?: return ActionResult.failed("invalid input event: $event")
        }

        Log.d(TAG, "actions = $actions")

        if (actions.isEmpty()) {
            return ActionResult.failed("no input action")
        }

        val worker = Worker()

        actions.forEach { action ->
            when (action) {
                is Action.Touch -> worker.performTouch(action)
                is Action.Swipe -> worker.performSwipe(action)
            }
        }

        worker.joinQuit()

        return ActionResult.success("OK")
    }

    private class Worker : HandlerThread("taa-dispatcher") {

        @SuppressLint("DiscouragedPrivateApi")
        companion object {

            private const val SWIPE_EVENT_PERIOD_MILLIS = 1000f / 60f  // 60Hz

            private val messages by lazy {
                MessageQueue::class.java.getDeclaredField("mMessages").apply {
                    isAccessible = true
                }
            }
        }

        private val handler by lazy {
            start()
            Handler(looper)
        }

        fun performTouch(action: Action.Touch) {
            val id = TouchSimulator.down(action.point.x, action.point.y)

            handler.postDelayed(action.duration) {
                TouchSimulator.up(id, action.point.x, action.point.y)
            }
        }

        fun performSwipe(action: Action.Swipe) {
            val numSegments = action.points.size - 1
            val segments = FloatArray(numSegments)
            var length = 0f

            for (i in 0 ..< numSegments) {
                val p1 = action.points[i]
                val p2 = action.points[i + 1]

                val dx = (p2.x - p1.x).toFloat()
                val dy = (p2.y - p1.y).toFloat()

                val dis = sqrt(dx * dx + dy * dy)

                segments[i] = dis
                length += dis
            }

            var duration = action.duration

            if (duration == 0L) {
                duration = (action.points.size - 1) * 200L
            }

            val numEvents = (duration / SWIPE_EVENT_PERIOD_MILLIS).toInt()
            val ts = SystemClock.uptimeMillis()

            val id = TouchSimulator.down(action.points[0].x, action.points[0].y)

            fun lerp(a: Int, b: Int, t: Float): Int {
                return (a.toFloat() + (b.toFloat() - a) * t).toInt()
            }

            for (i in 1 .. numEvents) {
                val target = length * i.toFloat() / numEvents

                var distance = 0f
                var index = 0

                while (index < numSegments && distance + segments[index] < target) {
                    distance += segments[index]
                    index++
                }

                val progress = if (segments[index] > 0) {
                    (target - distance) / segments[index]
                } else {
                    0f
                }

                val p1 = action.points[index]
                val p2 = action.points[index + 1]
                val x = lerp(p1.x, p2.x, progress)
                val y = lerp(p1.y, p2.y, progress)

                val time = ts + (i * SWIPE_EVENT_PERIOD_MILLIS).toLong()

                handler.postAtTime(time) {
                    TouchSimulator.move(id, x, y)
                }
            }

            handler.postAtTime(ts + duration) {
                val point = action.points.last()

                TouchSimulator.move(id, point.x, point.y)

                if (action.stabilize == 0L) {
                    TouchSimulator.up(id, point.x, point.y)
                } else {
                    handler.postDelayed(action.stabilize) {
                        TouchSimulator.up(id, point.x, point.y)
                    }
                }
            }
        }

        fun joinQuit() {
            val queue = looper.queue

            queue.addIdleHandler {
                synchronized(queue) {
                    if (messages.get(queue) == null) {
                        quitSafely()
                        false
                    } else {
                        true
                    }
                }
            }

            join()
        }
    }
}