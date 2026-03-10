package xyz.mufanc.taa.input

import android.graphics.Point
import android.hardware.input.InputManagerHidden
import android.os.SystemClock
import android.view.InputDevice
import android.view.InputEvent
import android.view.MotionEvent
import dev.rikka.tools.refine.Refine

object TouchSimulator {

    private const val DEFAULT_META_STATE = 0
    private const val DEFAULT_BUTTON_STATE = 0
    private const val DEFAULT_PRECISION_X = 1f
    private const val DEFAULT_PRECISION_Y = 1f
    private const val DEFAULT_EDGE_FLAGS = 0
    private const val DEFAULT_INPUT_SOURCE = InputDevice.SOURCE_TOUCHSCREEN
    private const val DEFAULT_DEVICE_ID = 0
    private const val DEFAULT_FLAGS = 0

    private val im: InputManagerHidden by lazy {
        Refine.unsafeCast(InputManagerHidden.getInstance())
    }

    private var downTime = 0L
    private val pointers = LinkedHashMap<Int, Point>()
    private var next = 0
    private val recycled = mutableSetOf<Int>()

    fun down(x: Int, y: Int): Int {
        val id = if (recycled.isNotEmpty()) {
            recycled.first().also { recycled.remove(it) }
        } else {
            next++
        }

        pointers[id] = Point(x, y)

        val ts = SystemClock.uptimeMillis()
        val action = if (pointers.size == 1) {
            downTime = ts
            MotionEvent.ACTION_DOWN
        } else{
            val index = pointers.size - 1
            MotionEvent.ACTION_POINTER_DOWN or (index shl MotionEvent.ACTION_POINTER_INDEX_SHIFT)
        }

        dispatchEvent(ts, action)

        return id
    }

    fun move(id: Int, x: Int, y: Int) {
        require(pointers.containsKey(id))
        pointers[id] = Point(x, y)

        val ts = SystemClock.uptimeMillis()

        dispatchEvent(ts, MotionEvent.ACTION_MOVE)
    }

    fun up(id: Int, x: Int, y: Int) {
        require(pointers.containsKey(id))
        pointers[id] = Point(x, y)

        val ts = SystemClock.uptimeMillis()
        val action = when {
            pointers.size == 1 -> {
                MotionEvent.ACTION_UP
            }
            else -> {
                val index = pointers.keys.indexOf(id)
                MotionEvent.ACTION_POINTER_UP or (index shl MotionEvent.ACTION_POINTER_INDEX_SHIFT)
            }
        }

        dispatchEvent(ts, action)
        pointers.remove(id)
        recycled.add(id)
    }

    private fun getInputDeviceId(): Int {
        val ids = InputDevice.getDeviceIds()

        for (id in ids) {
            val dev = InputDevice.getDevice(id)
            if (dev?.supportsSource(DEFAULT_INPUT_SOURCE) == true) {
                return id
            }
        }

        return DEFAULT_DEVICE_ID
    }

    private fun dispatchEvent(ts: Long, action: Int) {
        val count = pointers.size
        val props = Array(count) { MotionEvent.PointerProperties() }
        val coords = Array(count) { MotionEvent.PointerCoords() }

        pointers.entries.forEachIndexed { index, entry ->
            props[index].apply { id = entry.key }
            coords[index].apply {
                x = entry.value.x.toFloat()
                y = entry.value.y.toFloat()
            }
        }

        val event = MotionEvent.obtain(
            downTime,
            ts,
            action,
            count,
            props,
            coords,
            DEFAULT_META_STATE,
            DEFAULT_BUTTON_STATE,
            DEFAULT_PRECISION_X,
            DEFAULT_PRECISION_Y,
            getInputDeviceId(),
            DEFAULT_EDGE_FLAGS,
            DEFAULT_INPUT_SOURCE,
            DEFAULT_FLAGS
        )

        injectInputEvent(event)
    }

    fun injectInputEvent(event: InputEvent, mode: Mode = Mode.WAIT_FOR_RESULT) {
        im.injectInputEvent(event, mode.code)
        (event as? MotionEvent)?.recycle()
    }

    @Suppress("unused")
    enum class Mode(val code: Int) {
        NONE(0),
        WAIT_FOR_RESULT(1),
        WAIT_FOR_FINISHED(2)
    }
}
