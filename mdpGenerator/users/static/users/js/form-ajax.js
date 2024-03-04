$(document).ready(function() {
    $('#signup-form').submit(function(e) {
        e.preventDefault();  // Empêche la soumission standard du formulaire
        $.ajax({
            url: $(this).attr('action'),  // Utilise l'URL du formulaire
            type: $(this).attr('method'),  // Utilise la méthode du formulaire (POST)
            data: $(this).serialize(),  // Sérialise les données du formulaire
            success: function(response) {
                if (response.errors) {
                    var errors = JSON.parse(response.errors); // Assurez-vous de la structure de 'response.errors'
                    var errorMessages = '';
                    for (var key in errors) {
                        errorMessages += errors[key] + '<br/>'; // Construction des messages d'erreur
                    }
                    $('#signup-errors').html(errorMessages); // Insertion des erreurs dans le DOM

                    // Ajout de l'effet "shake" à la div du formulaire
                    $('#signup-form').effect("shake", {
                        times: 4,
                        distance: 20
                    }, 1000);
                } else {
                    window.location.href = '/home/';
                }
            },
            error: function(xhr, errmsg, err) {
                // Gestion des erreurs HTTP
                console.log("Une erreur est survenue : " + errmsg);
            }
        });
    });
});
