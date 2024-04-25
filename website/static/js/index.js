$('#abc').load(' #abc');
var timeout = setInterval(reloadDF, 5000);
function reloadDF () {
$('#abc').load(' #abc');
}


function deleteNote(noteId) {
  fetch("/delete-note", {
    method: "POST",
    body: JSON.stringify({ noteId: noteId }),
  }).then((_res) => {
    window.location.href = "/stocks";
  });
}
