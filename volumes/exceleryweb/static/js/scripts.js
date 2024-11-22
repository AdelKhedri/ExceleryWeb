function toggleElementId(el) {
    document.getElementById(el).classList.toggle('hidden')
}

function toggleTabElements(tabs, target_tabs,) {
    for(let i in tabs) {
        document.getElementById(i).classList.add('hidden');
        document.getElementById(tabs[i]).classList.remove('bg-gray-300');
    }
    for (let i in target_tabs){
        t1 = document.getElementById(i).classList.remove('hidden');
        t2 = document.getElementById(target_tabs[i]).classList.add('bg-gray-300');
    }
}

function toggleHideElementId(el) {
    let display = document.getElementById(el)
    if (display.style.display == 'none') {
        display.style.display = 'block';
    } else {
        display.style.display = 'none';
    }
}
function addFiledMessage(index) {
    let status = document.getElementById(`upload-file-status-${index}`)
    let icon_status = document.getElementById(`upload-file-status-icon${index}`);
    progress_bar = document.getElementById(`current-percentage-width-${index}`);
    status.innerText = 'Upload Failed';
    status.classList.remove('text-yellow-600')
    status.classList.add('text-red-600')
    icon_status.classList.remove('fa-circle-check');
    icon_status.classList.remove('text-green-500');
    icon_status.classList.add('fa-trash');
    icon_status.classList.add('text-red-600');

    progress_bar.classList.remove('bg-green-700');
    progress_bar.classList.add('bg-red-600');
    'bg-red-600'
}
function uploadFile(file, index, csrf) {
    const form = new FormData();
    form.append('file', file);

    file_explore.innerHTML += `
        <div class="flex items-center bg-white my-2 xl:w-10/12 lg:w-4/5 md:w-10/12 w-full px-3 py-1 rounded-3xl outline outline-4 outline-sky-200 shadow-md shadow-gray-800 my-1">
            <i class="fa-regular fa-file-arrow-up text-blue-700 text-xl p-[12px] px-[15px] w-fit bg-blue-100 rounded-full"></i>
            <div class="w-full mr-3">
                <div class="flex items-center justify-between my-2">
                    <p class="text-gray-800">${file.name}</p>
                    <i id="upload-file-status-icon${index}" class="fa-sharp fa-solid fa-circle-check text-green-500"></i>
                </div>
                <div class="w-full h-2 rounded-2xl bg-gray-200 ">
                    <div id="current-percentage-width-${index}" style="width: 0%" class="h-2 bg-orange-500 rounded-2xl"></div>
                </div>
                <div class="flex justify-between mt-1 mb-3">
                    <p id="upload-file-status-${index}" class="text-yellow-600">درحال انجام ...</p>
                    <p id="upload-file-status-percentage-${index}" class="text-sm">0%</p>
                </div>
            </div>
        </div>
    `;
    axios.post(
        '/',
        form,
        {
            headers: {
                'X-CSRFToken': `${csrf}`,
                'Content-Type': 'multipart/form-data'
            },
            onUploadProgress: function(event) {
                    const percentCompleted = Math.round((event.loaded / event.total) * 100);
                    document.getElementById(`upload-file-status-percentage-${index}`).innerHTML = `${percentCompleted}`;
                    progress_bar = document.getElementById(`current-percentage-width-${index}`);
                    progress_bar.style.width = `${percentCompleted}%`;
                    progress_bar.classList.remove('bg-yellow-600');
                    progress_bar.classList.add('bg-green-700');
                    // current_percentage_1.classList.remove('w-');
                if (percentCompleted == 100){
                    document.getElementById(`upload-file-status-${index}`).innerHTML = 'Upload Successfull';
                };
            }
        }
    ).then (function(respons) {
        if (respons.data == 'success'){
            let status = document.getElementById(`upload-file-status-${index}`)
            status.innerText = 'Upload successfull';
            status.classList.remove('text-yellow-600')
            status.classList.add('text-green-600')
        } else {
            addFiledMessage(index);

            const fileError = respons.data;
            let errorMessages = '';
            for (let field in fileError) {
                errorMessages += `<p class="text-red-600 text-center"><strong>${field}</strong>: <span class="text-black">${fileError[field]}</span></p>`;
            }
            errorSection.innerHTML = errorMessages;
        }
    }).catch(function(err) {
        addFiledMessage(index);
    })
}

function getUniqeueIndex(index=null) {
    if (index){
        if (indexFiles.includes(index)) {
            index = Math.floor(Math.random() * 1000)+1;
            return getUniqeueIndex(index);
        } else {
            indexFiles.push(index)
            return index
        }
    } else {
        index = Math.floor(Math.random() * 1000)+1;
        return getUniqeueIndex(index)
    }
}

function validateFile(file) {
    let file_error = {has_error: false, msg: ''}
    let file_size = 1024 * 1024 * 50
    const file_extention = file.name.slice(file.name.lastIndexOf('.'))
    const allow_extentions = ['.csv', '.xls', '.xlsx']
    if (!allow_extentions.includes(file_extention)) {
        file_error.has_error = true;
        file_error.msg = `File extention not allowed. only ${allow_extentions}`;
    }
    if (file.size> file_size) {
        file_error.has_error = true;
        file_error.msg = `size must less than ${file_size}`;
    }

    return file_error
}