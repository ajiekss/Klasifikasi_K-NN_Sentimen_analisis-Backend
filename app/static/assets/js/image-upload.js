// var img = $('.img-preview');

// function readfichier(e) {
//     if(window.FileReader) {
//         var label_img = document.querySelector('.custom-file-label');
//         var file  = e.target.files[0];
//         label_img.textContent = file.name;
//         var reader = new FileReader();
//         if (file && file.type.match('image.*')) {
//             reader.readAsDataURL(file);
//         } else {
//             img.attr('src', '');
//         }
//         reader.onloadend = function (e) {
//             img.attr('src', reader.result);
//         }
//     }
//   }

//   document.getElementById('images').addEventListener('change', readfichier, false);