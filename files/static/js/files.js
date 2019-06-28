
/* Выполняет ajax-запрос, вызывает onSuccess при успешном ответе. */
function ajax(conf) {
	var xmlhttp = new XMLHttpRequest();


	xmlhttp.onreadystatechange = function() {
		if (xmlhttp.readyState === XMLHttpRequest.DONE) {
			var resp = JSON.parse(xmlhttp.responseText);
			return conf.onSuccess(resp);
		} else {
			return conf.onError();
		}
	};

	xmlhttp.open(conf.type, conf.url, true);
	xmlhttp.setRequestHeader("X-Requested-With", 'XMLHttpRequest');
	if (conf.file) {
		xmlhttp.setRequestHeader("X-File-Name", conf.file.name);
		xmlhttp.setRequestHeader("X-File-Size", conf.file.size);
		xmlhttp.setRequestHeader("X-File-Type", conf.file.type);
	}
	xmlhttp.send(conf.content);
}

/* Обработчик события "клик по кнопке" */
function handleClickEvent(elem, callback) {
	if (elem.addEventListener) {
		elem.addEventListener('click', callback, false);
	} else if (elem.attachEvent) {
		elem.attachEvent('onclick', callback);
	}
}


/* Добавляет строку в таблицу */
function addTableRow(table, row, url_to_del, csrf) {
	var tr = '<tr class="files-row" id="f-row-'+ row.id +'">'
		+ '<td class="file-name-outer"><a class="file-name" href="'+ row.url +'">'+ row.name +'</a></td>'
		+ '<td class="file-size">'+ row.size +'</td>'
		+ '<td class="buttons">'
		+ '<form method="post" action="'+ url_to_del +'">'
		+ '<input type="hidden" name="csrfmiddlewaretoken" value="'+ csrf +'"'
		+ '<input type="hidden" name="filename" value="'+ row.name +'"  class="file-del-filename">'
		+ '<button type="submit" class="file-del">Удалить (без ajax)</button>'
		+ '<button type="button" class="file-del-ajax" id="f-del-'+ row.id +'">Удалить (ajax)</button>'
		+ '</form>'
		+ '</td></tr>';

	table.insertAdjacentHTML('beforeend', tr);
}

/* Получает список файлов ajax-запросом и перерисовывает таблицу. */
function reloadFilesTable() {
	// Получаем по ajax новое содержимое:
	ajax({
		type: 'GET',
		url: window.location.href,
		content: '',
		onSuccess: function (data) {
			// Удаляем все имеющиеся строки
			var table = document.getElementById('f-list-table');
			var old_rows = table.getElementsByClassName('files-row');

			while (old_rows.length > 0) {
				table.removeChild(old_rows[0]);
			}

			// Добавляем новые строки:
			for (var i in data) {
				addTableRow(table, data[i]);
			}
		},
		onError: function () {
			console.log('Error: can not get file list.')
		}
	});
}


/* Обработка событий */
document.addEventListener('DOMContentLoaded', function() {
	// Обработка кнопки "Добавить файл"
	var form = document.getElementById('f-add-form');
	var fileInput = document.getElementById('f-add-input');
	var addButton = document.getElementById('f-add-btn');

	var csrf = document.getElementsByName('csrfmiddlewaretoken')[0].value;

	handleClickEvent(addButton, function() {
		if (!fileInput.files) {
			console.log('There is no file for upload to server');
			return;
		}
		var file = fileInput.files[0],
			url = form.action,
			formData = new FormData();
		formData.append('file', file, file.name);
		formData.append('csrfmiddlewaretoken', csrf);

		ajax({
			type: 'POST',
			url: url,
			content: formData,
			file: file,
			onSuccess: function (result) {
				console.log('File '+file.name+' was added.');
				reloadFilesTable();
			},
			onError: function () {
				console.log('Error: can not upload file.')
			}
		});

	});


	// Обработка кнопок "Удалить файл"
	var table = document.getElementById('f-list-table');
	var delForm = table.getElementsByClassName('file-del-form')[0];
	var url = delForm.action;

	handleClickEvent(table, function(e) {
		// Добавляем событие onclick на ближайшего стабильного родителя, т.к. остальное - меняется.
		if (e.target && e.target.className === 'file-del-ajax') {
			var filename = e.target.parentElement.getElementsByClassName('file-del-filename')[0].value;
			var formData = new FormData();
			formData.append('filename', filename);
			formData.append('csrfmiddlewaretoken', csrf);
			ajax({
				type: 'POST',
				url: url,
				content: formData,
				onSuccess: function (result) {
					console.log('File '+filename+' was removed.');
					reloadFilesTable();
				},
				onError: function () {
					console.log('Error: can not remove file.')
				}

			})
		}
	})




});


