var attr_button_count = new Map();

function filterRankingTable(id_btn){
    var table, tr, i, heroes_spec;
    table = document.getElementById('table_ranking_body');
    tr = table.getElementsByTagName('tr');

    for (i = 0; i < tr.length; i++) {
        heroes_spec = tr[i].getElementsByTagName("th")[2];
        if (heroes_spec) {
            if(attr_button_count.get(id_btn) % 2 == 0) {
                tr[i].style.display = "";
            }
            else {
                var attr_row = heroes_spec.getElementsByTagName("p")[1].innerText.split(',')[0]
                var attr_button = id_btn.split('_')[0].toUpperCase()
                if (attr_row != attr_button) {
                    tr[i].style.display = "none";
                } else {
                    tr[i].style.display = "";
                }
            }
        }
    }
}


function setOpacityButton(id_btn) {
    if (attr_button_count.has(id_btn)) {
        attr_button_count.set(
            id_btn,
            attr_button_count.get(id_btn) + 1
        );
    }
    else {
        attr_button_count.set(id_btn, 1);
    }
    filterRankingTable(id_btn);
    var attr_button_list = document.getElementsByClassName('attr_button');
    var attr_button_id;
    var attr_button;
    for (attr_button_id=0; attr_button_id < attr_button_list.length; attr_button_id++) {
        attr_button = attr_button_list[attr_button_id];
        if ((id_btn == attr_button.id) && (attr_button_count.get(id_btn) % 2 != 0)) {
            attr_button.style.opacity = 1;
        }
        else {
            attr_button.style.opacity = 0.3;
            attr_button_count.set(
                attr_button.id,
                0
            );
        }

    }
}

function sortTable(id_btn) {
    var table, rows, switching, i, x, y, shouldSwitch;
    table = document.getElementById("table_rank");
    switching = true;
    /* Make a loop that will continue until
    no switching has been done: */
    while (switching) {
      // Start by saying: no switching is done:
      switching = false;
      rows = table.rows;
      /* Loop through all table rows (except the
      first, which contains table headers): */
      for (i = 1; i < (rows.length - 1); i++) {
        // Start by saying there should be no switching:
        shouldSwitch = false;
        /* Get the two elements you want to compare,
        one from current row and one from the next: */
        if (id_btn == "win_rate_rank") {
            x = parseFloat(rows[i].getElementsByTagName("th")[4].innerHTML.replace('%', ''));
            y = parseFloat(rows[i + 1].getElementsByTagName("th")[4].innerHTML.replace('%', ''));
        } else if (id_btn == "pick_rate_rank") {
            x = parseFloat(rows[i].getElementsByTagName("th")[5].innerHTML.replace('%', ''));
            y = parseFloat(rows[i + 1].getElementsByTagName("th")[5].innerHTML.replace('%', ''));
        } else {
            x = Math.pow(parseFloat(rows[i].getElementsByTagName("th")[4].innerHTML.replace('%', '')), 2) * parseFloat(rows[i].getElementsByTagName("th")[5].innerHTML.replace('%', ''));
            y = Math.pow(parseFloat(rows[i + 1].getElementsByTagName("th")[4].innerHTML.replace('%', '')), 2) * parseFloat(rows[i + 1].getElementsByTagName("th")[5].innerHTML.replace('%', ''))
        }
        // Check if the two rows should switch place:
        if (x < y) {
          // If so, mark as a switch and break the loop:
          shouldSwitch = true;
          break;
        }
      }
      if (shouldSwitch) {
        /* If a switch has been marked, make the switch
        and mark that a switch has been done: */
        rows[i].parentNode.insertBefore(rows[i + 1], rows[i]);
        switching = true;
      }
    }
  }

function setColorRank(id_btn) {
    var rank_button_list = document.getElementsByClassName('rank_button');
    var rank_button_id;
    var rank_button;
    for (rank_button_id=0; rank_button_id < rank_button_list.length; rank_button_id++) {
        rank_button = rank_button_list[rank_button_id];
        if (id_btn == rank_button.id) {
            rank_button.style.borderBottom = '5px solid var(--clr-rank-selected)';
            rank_button.style.fontWeight = 'bold';
            rank_button.style.color = 'var(--clr-rank-selected)';
        }
        else {
            rank_button.style.borderBottom = "none";
            rank_button.style.fontWeight = "none";
            rank_button.style.color = "var(--clr-gray-light)";
        }

    }
    sortTable(id_btn);
}

