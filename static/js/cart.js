function changeQty(button, delta) {
  // 1. Знаходимо форму, де була натиснута кнопка
  const form = button.closest('form');

  // 2. Знаходимо інпут з кількістю
  const input = form.querySelector('input[name="qty"]');

  // 3. Перетворюємо значення на число
  let value = parseInt(input.value || '0', 10);

  // 4. Якщо значення не число — ставимо 0
  if (isNaN(value)) {
    value = 0;
  }

  // 5. Змінюємо кількість на +1 або -1
  value += delta;

  // 6. Не дозволяємо негативні значення
  if (value < 0) value = 0;

  // 7. Повертаємо нове значення у поле
  input.value = value;

  // 8. Автоматично відправляємо форму POST
  form.submit();
}

