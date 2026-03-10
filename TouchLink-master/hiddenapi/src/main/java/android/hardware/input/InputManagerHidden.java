package android.hardware.input;

import android.view.InputEvent;

import dev.rikka.tools.refine.RefineAs;

@RefineAs(InputManager.class)
public class InputManagerHidden {

    public static InputManager getInstance() {
        throw new RuntimeException("Stub!");
    }

    public boolean injectInputEvent(InputEvent event, int mode) {
        throw new RuntimeException("Stub!");
    }
}
