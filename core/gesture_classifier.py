def is_fist(lm):
    return lm[8].y > lm[6].y and lm[12].y > lm[10].y

def is_palm(lm):
    return (
        lm[8].y < lm[6].y and
        lm[12].y < lm[10].y and
        lm[16].y < lm[14].y and
        lm[20].y < lm[18].y
    )

def is_peace(lm):
    return (
        lm[8].y < lm[6].y and
        lm[12].y < lm[10].y and
        lm[16].y > lm[14].y
    )

def finger_up(tip, pip):
    # Finger is up if tip is above pip (y-axis)
    return tip.y < pip.y


def classify_gesture(lm):
    """
    lm: list of 21 MediaPipe landmarks
    returns: gesture string
    """

    # Finger states
    index_up  = finger_up(lm[8], lm[6])
    middle_up = finger_up(lm[12], lm[10])
    ring_up   = finger_up(lm[16], lm[14])
    pinky_up  = finger_up(lm[20], lm[18])

    # Thumb: use y comparison to avoid left/right issues
    thumb_up = lm[4].y < lm[3].y

    # -------------------------------
    # ✊ FIST → COPY
    # -------------------------------
    if not any([thumb_up, index_up, middle_up, ring_up, pinky_up]):
        return "COPY"

    # -------------------------------
    # 🖐 PALM → PASTE
    # -------------------------------
    if all([index_up, middle_up, ring_up, pinky_up]):
        return "PASTE"

    # -------------------------------
    # ✌️ PEACE → SCROLL DOWN
    # -------------------------------
    if index_up and middle_up and not ring_up and not pinky_up:
        return "SCROLL_DOWN"

    # -------------------------------
    # ☝️ INDEX ONLY → SCROLL UP
    # -------------------------------
    if index_up and not any([middle_up, ring_up, pinky_up, thumb_up]):
        return "SCROLL_UP"

    # -------------------------------
    # 👍 THUMBS UP → CLOSE WINDOW
    # -------------------------------
    if thumb_up and not any([index_up, middle_up, ring_up, pinky_up]):
        return "CLOSE"

    return "NONE"
