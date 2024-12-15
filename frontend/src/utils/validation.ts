// src/utils/validation.ts

export const validateZones = (
  selectedOptions: any[],
  zoneError: { value: string }
) => {
  console.log(selectedOptions.length);
  if (selectedOptions.length === 0) {
    zoneError.value = "Нужно выбрать хотя бы одну зону!";
  } else {
    zoneError.value = "";
  }
};

export const validateMinCountChar = (
  min_count_char: { value: number | null },
  minCountError: { value: string }
) => {
  if (
    min_count_char.value === null ||
    min_count_char.value === undefined ||
    String(min_count_char.value) === ""
  ) {
    minCountError.value =
      "Минимальное количество символов не должно быть пустым.";
  } else if (!Number.isInteger(min_count_char.value)) {
    minCountError.value =
      "Минимальное количество символов должно быть целым числом.";
  } else if (min_count_char.value < 20 || min_count_char.value > 80) {
    minCountError.value =
      "Минимальное количество символов должно быть от 20 до 80.";
  } else {
    minCountError.value = "";
  }
};

export const validateMaxCountChar = (
  max_count_char: { value: number | null },
  min_count_char: { value: number | null },
  maxCountError: { value: string }
) => {
  let upperBound = null;
  if (min_count_char.value !== null) {
    upperBound = min_count_char.value + 9;
  }

  if (
    max_count_char.value === null ||
    max_count_char.value === undefined ||
    String(max_count_char.value) === ""
  ) {
    maxCountError.value =
      "Максимальное количество символов не должно быть пустым.";
  } else if (!Number.isInteger(max_count_char.value)) {
    maxCountError.value =
      "Максимальное количество символов должно быть целым числом.";
  } else if (max_count_char.value < 20 || max_count_char.value > 80) {
    maxCountError.value =
      "Максимальное количество символов должно быть от 20 до 80.";
  } else if (
    min_count_char.value !== null &&
    max_count_char.value < Number(min_count_char.value) + 10 // Исправлено на +10
  ) {
    console.log(max_count_char.value < min_count_char.value + 10);
    console.log("max_count_char:", max_count_char.value);
    console.log("min_count_char:", min_count_char.value);
    maxCountError.value =
      "Максимальное количество символов должно быть больше минимального на 10.";
  } else {
    maxCountError.value = "";
  }
};

export const validateTimePressKey = (
  time_press_key: { value: number | null },
  timePressError: { value: string }
) => {
  if (
    time_press_key.value === null ||
    time_press_key.value === undefined ||
    String(time_press_key.value) === ""
  ) {
    timePressError.value = "Время нажатия на клавишу не должно быть пустым.";
  } else if (time_press_key.value < 0.5 || time_press_key.value > 1.5) {
    timePressError.value =
      "Время нажатия на клавишу должно быть от 0.5 до 1.5.";
  } else {
    timePressError.value = "";
  }
};

// Новые функции валидации
export const validateLengthExercise = (
  lengthExercise: { value: number | string },
  minCount: number,
  maxCount: number,
  lengthError: { value: string }
) => {
  const length = Number(lengthExercise.value);
  if (length < minCount || length > maxCount) {
    lengthError.value = `Количество символов должно быть от ${minCount} до ${maxCount}.`;
  } else {
    lengthError.value = "";
  }
};

export const validateTextExercise = (
  textExercise: { value: string },
  minCount: number,
  maxCount: number,
  textError: { value: string }
) => {
  const length = textExercise.value.length; // Получаем длину текста
  if (length < minCount) {
    textError.value = `Текст упражнения должен содержать минимум ${minCount} символов.`;
  } else if (length > maxCount) {
    textError.value = `Текст упражнения не должен превышать ${maxCount} символов.`;
  } else {
    textError.value = ""; // Если длина текста в допустимых пределах, очищаем ошибку
  }
};

export const validateLogin = (value: string, loginError: { value: string }) => {
  if (value.length < 4) {
    loginError.value = "Логин должен содержать минимум 4 символа.";
  } else if (value.length > 10) {
    loginError.value = "Логин не может превышать 10 символов.";
  } else {
    loginError.value = ""; // Устанавливаем пустую строку, если ошибок нет
  }
};

export const validatePassword = (
  value: string,
  passwordError: { value: string }
) => {
  if (value.length < 4) {
    passwordError.value = "Пароль должен содержать минимум 4 символа.";
  } else if (value.length > 10) {
    passwordError.value = "Пароль не может превышать 10 символов.";
  } else {
    passwordError.value = ""; // Устанавливаем пустую строку, если ошибок нет
  }
};

export const validateRepeatPassword = (
  repeatPassword: string,
  password: string,
  repeatPasswordError: { value: string }
) => {
  if (repeatPassword !== password) {
    repeatPasswordError.value = "Пароли не совпадают.";
  } else {
    repeatPasswordError.value = "";
  }
};
