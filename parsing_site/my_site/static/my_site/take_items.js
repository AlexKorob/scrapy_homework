$(function() {

  var excludes = [];
  var limit_call = 5;

  $(document).on("click", "#parse-button", function(e) {
    e.preventDefault();
    let csrftoken = $("[name=csrfmiddlewaretoken]").val();

    $.ajaxSetup({
      beforeSend: function(xhr, settings) {
          if (!this.crossDomain) {
              xhr.setRequestHeader("X-CSRFToken", csrftoken);
          }
      }
    });

    let url = $("input[name='url']").val();

    $.ajax({
      type: "POST",
			url: window.location.pathname,
			data: {"url": url},
			cache: false,
      datatype: 'json',
      success: function(data, status) {
        console.log(status);

        if (data != "success") {
            let error = data;
            $("<p>").attr({
              class: "error",
              style: "color: red;",
            }).text(error).insertBefore($("input[name='url']"));
        }
        else {
          if ($(".error")) {
            $(".error").remove();
            // $("#parse-button").prop("disabled", true);
            $(".data").html("");
            limit_call = 5;
            excludes = [];
            $(".parse>p").empty();
            $("<p>").text("Парсинг начался пожалуйста подождите...").appendTo(".parse");
            getData();
          }
        }
      },
      error: function(err) {
        console.log(err.responseText);
      },
    });
  });

  function getData() {
    setTimeout(getDataFromServer, 5000);
  }

  function getDataFromServer() {

    let url = $("input[name='url']").val();

    $.ajax({
      type: "GET",
      url: window.location.pathname,
      data: {"get_data": "True", "url": url, "excludes": JSON.stringify(excludes)},
      cache: false,
      success: function(data) {

        for (var id in data) {
          excludes.push(id);
          var card = $("<div>").attr({
            id: id,
            class: "card",
          });

          let items = data[id];
          $("<p>").text(items["title"]).appendTo(card);
          $("<p>").text(items["company"]).appendTo(card);
          $("<p>").text(items["category"]).appendTo(card);
          $("<p>").text(items["price"]).appendTo(card);
          let slider_container = $("<div>").attr({
            class: "slider-container"
          });
          for (img_url in items["images"]) {
            $("<img>").attr({
              src: items["images"][img_url],
              alt: "None",
            }).appendTo(slider_container);
          }
          slider_container.appendTo(card);
          slider_container.slick();

          let sizes = "";
          for (size in items["sizes"]) {
            sizes += items["sizes"][size] + " ";
          }
          $("<p>").text(sizes).appendTo(card);

          $("<p>").html("<b>Description</b>").appendTo(card);
          let description = $("<div>").attr({class: "description"})
          $(description).html(items["description"]).appendTo(description);
          $(description).appendTo(card);
          card.appendTo($(".data"));
        }

        if (limit_call > 0) {
          limit_call -= 1;
          getData();
        }
        // if after 5 request not all data take from server, run this ajax again
        else if (JSON.stringify(data) != "{}") {
          getData();
        }
        else {
          $(".parse>p").empty();
          $("<p>").attr({
            style: "font-size: 20px; color: green; text-align: center",
          }).text("Парсинг Завершен").appendTo(".parse");
        }
      },
      error: function(err) {
        console.log(err.responseText);
      },
    });
  }


});
