(function () {
  const form = document.getElementById("invoice-form");
  if (!form) return;

  const prefix = form.dataset.prefix; // ex: "items"
  const addBtn = document.getElementById("add-row");
  const tbody = document.getElementById("items-body");
  const tpl = document.getElementById("empty-row-template");

  // TOTAL_FORMS est un champ caché généré par Django
  const totalFormsInput = document.getElementById(`id_${prefix}-TOTAL_FORMS`);

  function countVisibleRows() {
    const rows = Array.from(document.querySelectorAll(".item-row"));
    return rows.filter((r) => {
      if (r.style.display === "none") return false;
      const del = r.querySelector(`input[name$="-DELETE"]`);
      return !(del && del.checked);
    }).length;
  }

  function wireRemoveButton(row) {
    const btn = row.querySelector(".js-remove-row");
    if (!btn) return;

    btn.addEventListener("click", () => {
      // Empêche d'avoir 0 ligne (UX), le serveur protège aussi
      if (countVisibleRows() <= 1) {
        alert("Une facture doit contenir au moins un produit.");
        return;
      }

      const deleteInput = row.querySelector(`input[name$="-DELETE"]`);
      if (deleteInput) deleteInput.checked = true;
      row.style.display = "none";
    });
  }

  function addRow() {
    const index = parseInt(totalFormsInput.value, 10);
    const html = tpl.innerHTML.replaceAll("__prefix__", String(index));

    const tmp = document.createElement("tbody");
    tmp.innerHTML = html.trim();
    const newRow = tmp.firstElementChild;

    tbody.appendChild(newRow);
    totalFormsInput.value = String(index + 1);

    wireRemoveButton(newRow);
  }

  // Active le bouton "retirer" sur les lignes déjà présentes
  document.querySelectorAll(".item-row").forEach(wireRemoveButton);

  addBtn.addEventListener("click", addRow);
})();
