async function get_preview_md(text) {
	const url = '/get_preview_md';
	let form_data = new FormData();
	form_data.append('text', text);

	let response = await fetch(url, {
		method: 'POST',
		body: form_data
	})
	if (response.ok) {
		let file_url = response.text()
		return file_url
	} else {
		console.log('Error is:', reponse.status)
	}
}