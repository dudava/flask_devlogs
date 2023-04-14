	function make_image_loader(div_id) {

		let drop_area = document.querySelector(`#${div_id}`)
		console.log(drop_area)
		drop_area.addEventListener('dragenter', handlerFunction, false)
		drop_area.addEventListener('dragleave', handlerFunction, false)
		drop_area.addEventListener('dragover', handlerFunction, false)
		drop_area.addEventListener('drop', handlerFunction, false)	

		drop_area.addEventListener('drop', handle_drop, false)

		function handlerFunction(e) {
			e.preventDefault()
			e.stopPropagation()
		}

		function handle_drop(e) {
			let dt = e.dataTransfer;
			console.log(dt)
			handle_files(dt);
		} 

		function handle_files(dt) {
			([...dt.files]).forEach(upload_files);
		}

		async function upload_files(file) {
			console.log(file)
			const url = '/upload_image';
			let form_data = new FormData();
			form_data.append('file', file);
			form_data.append('image_name', file.name)

			let response = await fetch(url, {
				method: 'POST',
				body: form_data
			})
			console.log(response)
			if (response.ok) {
				let text = await response.text()
				drop_area.value += `\n${text}`
				console.log(text)
			} else {
				console.log('Error is:', reponse.status)
			}
		}


		['dragenter', 'dragover'].forEach(eventName => {
		  drop_area.addEventListener(eventName, highlight, false)
		});
		['dragleave', 'drop'].forEach(eventName => {
		  drop_area.addEventListener(eventName, unhighlight, false)
		});

		function highlight(e) {
		  drop_area.classList.add('highlight')
		}
		function unhighlight(e) {
		  drop_area.classList.remove('highlight')
		}
	}