$(document).ready(function () {
  $("li[name='object_info']").click(function () {
    $("li[name='object_info']").next().removeClass("active");
    $(this).next().addClass("active");
    $("#form-post").addClass("active");
    let currentInput = $(this).val();
    let firstname = $(this).attr("firstname");
    let lastname = $(this).attr("lastname");
    $("#member_id2").val(currentInput);
    $("#member_id2").attr("value", currentInput);
    $("#firstName").val(firstname);
    $("#lastName").val(lastname);
    $("#firstName").attr("value", firstname);
    $("#lastName").attr("value", lastname);
    console.log(currentInput)
  });
  $(".navbar-toggler").click(function () {
    $(".navbar-collapse").toggleClass("expand");
  });
  $(".reg-form").click(function () {
    $(".loading-screen").addClass("active");
  });

  //Loop through all the children and check if the url is equal to the page current page url
  $(".navbar-nav .navList")
    .children()
    .each(function () {
      if (this.href == document.URL) {
        $(this).addClass("active");
      }
    });
  // add 'activate' class to slowly show login form and others
  $(".container-edit").addClass("activate");
  $(".form-main").addClass("activate");

  // used to filter update_giving_list
  $(document).ready(function () {
    $("#myInput").on("keyup", function () {
      var value = $(this).val().toLowerCase();
      $("#myTable tr").filter(function () {
        $(this).toggle($(this).text().toLowerCase().indexOf(value) > -1);
      });
    });
  });
});
