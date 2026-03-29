if (!localStorage.getItem('loggedIn')) {
  window.location.href = '/normal/login.html';
}

function logout() {
  localStorage.removeItem('loggedIn');
  window.location.href = '/normal/login.html';
}

let students = JSON.parse(localStorage.getItem('students') || '[]');
let nextId = students.length ? Math.max(...students.map(s => s.id)) + 1 : 1;

function addStudent() {
  let name = document.getElementById('name').value.trim();
  let course = document.getElementById('course').value.trim();
  if (!name || !course) return alert('Name aur Course dono bharo!');

  students.push({ id: nextId++, name, course });
  localStorage.setItem('students', JSON.stringify(students));
  document.getElementById('name').value = '';
  document.getElementById('course').value = '';
  load();
}

function load() {
  let list = document.getElementById('list');
  list.innerHTML = '';
  students.forEach(s => {
    list.innerHTML += `<li class="list-group-item d-flex justify-content-between">
      ${s.name} - ${s.course}
      <button onclick="del(${s.id})" class="btn btn-sm btn-danger">X</button>
    </li>`;
  });
}

function del(id) {
  students = students.filter(s => s.id !== id);
  localStorage.setItem('students', JSON.stringify(students));
  load();
}

load();
