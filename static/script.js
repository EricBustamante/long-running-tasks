function myFunction() {
    $.ajax({
        url: 'long-task',
        method: 'POST',
        headers: { 'User-Id': '55a5f921-0541-4394-ba6f-6ba79678bf2c' },
        success: function (data, status) {
            alert("Data: " + data + "\nStatus: " + status);
            pollTask(data)
        }
    });
}

function pollTask(taskId) {
    $.get("long-task/" + taskId, function (data, statusText, xhr) {
        if (xhr.status == 202) {
            setTimeout(function() { 
                pollTask(taskId); }, 5000);
        }
        else if(xhr.status == 200) {
            var newResult = $("<p></p>");
            newResult.html(data);
            $(".results").append(newResult);
        }
    });
}