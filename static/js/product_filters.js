function updateFilterControls() {
    const category = document.querySelector('select[name="category"]');
    const brand    = document.querySelector('select[name="brand"]');
    const author   = document.querySelector('select[name="author"]');
    const size     = document.querySelector('select[name="size"]');

    if (!category || !brand || !author || !size) {
      return;
    }

    // 1) Увімкнути все перед логікою
    brand.disabled  = false;
    author.disabled = false;
    size.disabled   = false;

    // 2) Якщо вибрана конкретна категорія
    if (category.value === "electronics") {
      author.value = "";
      size.value   = "";
      author.disabled = true;
      size.disabled   = true;
      return;
    }

    if (category.value === "books") {
      brand.value = "";
      size.value  = "";
      brand.disabled = true;
      size.disabled  = true;
      return;
    }

    if (category.value === "clothing") {
      brand.value  = "";
      author.value = "";
      brand.disabled  = true;
      author.disabled = true;
      return;
    }

    // 3) Категорія = "All categories", але вибрали інші фільтри
    if (!category.value) {

      if (brand.value) {
        // brand -> electronics
        category.value = "electronics";
        author.value = "";
        size.value   = "";
        author.disabled = true;
        size.disabled   = true;
      }

      else if (author.value) {
        // author -> books
        category.value = "books";
        brand.value = "";
        size.value  = "";
        brand.disabled = true;
        size.disabled  = true;
      }

      else if (size.value) {
        // size -> clothing
        category.value = "clothing";
        brand.value  = "";
        author.value = "";
        brand.disabled  = true;
        author.disabled = true;
      }
    }
}

document.addEventListener("DOMContentLoaded", function () {
    const category = document.querySelector('select[name="category"]');
    const brand    = document.querySelector('select[name="brand"]');
    const author   = document.querySelector('select[name="author"]');
    const size     = document.querySelector('select[name="size"]');

    if (category) category.addEventListener("change", updateFilterControls);
    if (brand)    brand.addEventListener("change", updateFilterControls);
    if (author)   author.addEventListener("change", updateFilterControls);
    if (size)     size.addEventListener("change", updateFilterControls);

    updateFilterControls();
});
