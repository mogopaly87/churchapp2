$(document).ready(function () {

  // on clicking the firstName link with name='object_id',
  $("#click-link a[name='object_info']").click(function (){
    // add 'active' class to posting form.
    // 'active' class changes form to display:block
    $("#form-post").addClass("active")
    $(".form-control-post").addClass("active")
    $(".form-control-3").addClass("active")

    // get data attributes for the firstName, LastName & ID
    var firstName = $(this).data("first-name");
    var lastName = $(this).data("last-name");
    var memberId = $(this).data("member-id");

    // assign data attributes to the value of inputs (firstName, lastName, member_id2)
    $("#firstName").val(firstName);
    $("#lastName").val(lastName);
    $("#member_id2").val(memberId);
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
  $(".journal-form-main").addClass("activate");
  // $("#update-container").addClass("activate");

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
