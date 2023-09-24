#include QMK_KEYBOARD_H

#ifdef RGB_MATRIX_ENABLE

bool rgb_matrix_indicators_user(void) {
    uint8_t layer = get_highest_layer(layer_state);
    if ((layer > 0) && (layer < 10)) { //Only works for layers 1 - 9 where 0 would be the default layer
        rgb_matrix_set_color(layer, 0xFF, 0xFF, 0xFF);  //Set the coresponding backlight in the number row on to show layer number
    }
    if (is_caps_word_on()) {
        rgb_matrix_set_color(30, 0xFF, 0xFF, 0xFF); // Turns on caps lock light if capsword is turned on
    }
    return true;
}
#endif