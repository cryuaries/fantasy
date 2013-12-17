
function post_to_url(path, params, method) {
    method = method || "post"; // Set method to post by default, if not specified.

    // The rest of this code assumes you are not using a library.
    // It can be made less wordy if you use one.
    var form = document.createElement("form");
    form.setAttribute("method", method);
    form.setAttribute("action", path);

    for(var key in params) {
        var hiddenField = document.createElement("input");
        hiddenField.setAttribute("type", "hidden");
        hiddenField.setAttribute("name", key);
        hiddenField.setAttribute("value", params[key]);

        form.appendChild(hiddenField);
    }

    document.body.appendChild(form);    // Not entirely sure if this is necessary
    form.submit();
}

function end_with(str, ends) {
    if (str.indexOf(ends) == (str.length - ends.length))
        return true;
    else
        return false;
}

function fantasy() {
    var url = window.location.href;
    if (!end_with(url, "/standings"))
    {
        alert("Please go to full standings page first.")
        return false;
    }
    body = document.body.innerHTML;
    head = document.getElementsByTagName('head')[0].innerHTML;
    post_to_url('http://fantasyahoo.appspot.com/fantasy', {'body': body, 'head': head});
    //post_to_url('http://localhost:8080/clone', {'body': body});
    return true;
}

fantasy()