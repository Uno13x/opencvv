import cv2 as cv
import mediapipe as mp
import numpy as np
import pyautogui

mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

camera = cv.VideoCapture(1)
rodando = True
digitando_l = False
digitando_o = False
digitando_a = False

ultimo_estado_dedo_l = False
ultimo_estado_dedo_o = False
ultimo_estado_dedo_a = False

with mp_hands.Hands(min_detection_confidence=0.8, min_tracking_confidence=0.5) as hands:
    while rodando:
        status, frame = camera.read()
        # BGR 2 RGB
        image = cv.cvtColor(frame, cv.COLOR_BGR2RGB)

        # Flip on horizontal
        image = cv.flip(image, 1)

        # Set flag
        image.flags.writeable = False

        # Detections
        results = hands.process(image)

        # Set flag to true
        image.flags.writeable = True

        # RGB 2 BGR
        image = cv.cvtColor(image, cv.COLOR_RGB2BGR)

        # Detections
        print(results)

        # Rendering results
        if results.multi_hand_landmarks:
            for num, hand in enumerate(results.multi_hand_landmarks):
                mp_drawing.draw_landmarks(image, hand, mp_hands.HAND_CONNECTIONS)


                dedo_do_meio_abaixado_l = hand.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y > hand.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_MCP].y


                if dedo_do_meio_abaixado_l and not ultimo_estado_dedo_l:
                    # Inicie ou continue a digitar 'L'
                    digitando_l = True
                    pyautogui.press('l')

                    # Desenhe 'L' na imagem
                    x = int(hand.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].x * image.shape[1])
                    y = int(hand.landmark[mp_hands.HandLandmark.MIDDLE_FINGER_TIP].y * image.shape[0])
                    cv.putText(image, 'L', (x, y), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv.LINE_AA)
                elif not dedo_do_meio_abaixado_l and ultimo_estado_dedo_l:
                    # Pare de digitar 'L'
                    digitando_l = False


                ultimo_estado_dedo_l = dedo_do_meio_abaixado_l

                dedo_fura_bolo_abaixado_o = hand.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y > hand.landmark[mp_hands.HandLandmark.INDEX_FINGER_MCP].y


                if dedo_fura_bolo_abaixado_o and not ultimo_estado_dedo_o:
                    # Inicie ou continue a digitar 'O'
                    digitando_o = True
                    pyautogui.press('o')

                    # Desenhe 'O' na imagem
                    x = int(hand.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x * image.shape[1])
                    y = int(hand.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y * image.shape[0])
                    cv.putText(image, 'O', (x, y), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv.LINE_AA)
                elif not dedo_fura_bolo_abaixado_o and ultimo_estado_dedo_o:
                    # Pare de digitar 'O'
                    digitando_o = False


                ultimo_estado_dedo_o = dedo_fura_bolo_abaixado_o


                dedo_anelar_abaixado_a = hand.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].y > hand.landmark[mp_hands.HandLandmark.RING_FINGER_MCP].y


                if dedo_anelar_abaixado_a and not ultimo_estado_dedo_a:

                    digitando_a = True
                    pyautogui.press('a')

                    # Desenhe 'A' na imagem
                    x = int(hand.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].x * image.shape[1])
                    y = int(hand.landmark[mp_hands.HandLandmark.RING_FINGER_TIP].y * image.shape[0])
                    cv.putText(image, 'A', (x, y), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2, cv.LINE_AA)
                elif not dedo_anelar_abaixado_a and ultimo_estado_dedo_a:
                    # Pare de digitar 'A'
                    digitando_a = False


                ultimo_estado_dedo_a = dedo_anelar_abaixado_a

        if not status or cv.waitKey(1) & 0xff == ord('q'):
            rodando = False

        cv.imshow("Camera", image)

cv.destroyAllWindows()