function titleRequired(){
    var empty = document.forms["addTaskForm"]["title"].value;
    empty= empty.trim();
    if (empty == ""|| empty == null){
    alert("Title field cannot be empty.");
    return false;
    }
    return true;
}