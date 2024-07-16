const userSelectedCategory = document.getElementById('inlineFormSelectPref');
const deleteButton = document.getElementById('delete_button');
const searchButton = document.getElementById('search_button');
const dataTable = document.getElementById('data-table');
const todaySpan = document.getElementById('today');

/**
 * 검색 Event 감지 및 필터링 셋업 함수
 */
function search() {
  document.getElementById('merchant_search_bar').addEventListener('input', function () {
    const searchText = this.value.toLowerCase();
    const selectedCategory = userSelectedCategory.value;
    filterDataByProductName(selectedCategory, searchText);
  });
}

/**
 * Gender Cell 생성 시, button element 생성해주는 함수
 * @param gender
 * @returns {HTMLButtonElement}
 */
function createGenderCell(gender) {
  const button = document.createElement('button');
  button.textContent = gender;
  button.disabled = true;  // 버튼을 비활성화하여 클릭되지 않도록 함
  if (gender === 'Men') {
    button.className = 'btn btn-light forMen';
  } else if (gender === 'Women') {
    button.className = 'btn btn-light forWomen';
  } else if (gender === 'Common') {
    button.className = 'btn btn-light';
  } else {
    button.className = 'btn btn-light';
  }
  return button;
}

/**
 * Product Cell 생성 시, mouseover, mouseleave event 추가해주는 함수
 */
function createProductCell(product) {
  const productCell = document.createElement('span');
  productCell.innerHTML = product;
  productCell.onmouseover = function () {
    productCell.style.color = 'red';
  }
  productCell.onmouseleave = function () {
    productCell.style.color = 'black';
  }
  return productCell;
}

/**
 * 테이블 생성 함수
 * @param item
 */
function createTableRow(item){
  const row = dataTable.insertRow();
  const checkboxCell = row.insertCell(0);
  const checkbox = document.createElement('input');
  checkbox.type = 'checkbox';
  checkboxCell.appendChild(checkbox);

  row.insertCell(1).innerHTML = item.category;
  row.insertCell(2).innerHTML = item.brand;
  const productCell = row.insertCell(3);
  productCell.appendChild(createProductCell(item.product));
  const genderCell = row.insertCell(4);
  genderCell.appendChild(createGenderCell(item.gender));
  row.insertCell(5).innerHTML = item.price;
}

/**
 * 카테고리 기준 필터링 함수
 * @param selectedCategory
 */
function filterData(selectedCategory) {
  // 필터링 하기 전에 테이블 초기화
  while (dataTable.rows.length > 0) {
    dataTable.deleteRow(0);
  }

  let categoryString;
  switch (selectedCategory) {
    case 'tops':
      categoryString = '상의';
      break;
    case 'bottoms':
      categoryString = '하의';
      break;
    case 'shoes':
      categoryString = '신발';
      break;
    case 'accessories':
      categoryString = '패션잡화';
      break;
    default:
      categoryString = '';
      break;
  }

  const rows = dataTable.getElementsByTagName('tr');
  for (let i = 0; i < rows.length; i++) {
    const row = rows[i];
    const categoryCell = row.cells[1];
    if (categoryString === '' || categoryCell.innerText === categoryString) {
      row.style.display = '';
    } else {
      row.style.display = 'none';
    }
  }
}

/**
 * 상품명 기준 필터링 함수
 * @param selectedCategory
 * @param searchText
 */
function filterDataByProductName(selectedCategory, searchText) {
  // 필터링 하기 전에 테이블 초기화
  while (dataTable.rows.length > 0) {
    dataTable.deleteRow(0);
  }

  let categoryString;
  switch (selectedCategory) {
    case 'tops':
      categoryString = '상의';
      break;
    case 'bottoms':
      categoryString = '하의';
      break;
    case 'shoes':
      categoryString = '신발';
      break;
    case 'accessories':
      categoryString = '패션잡화';
      break;
    default:
      categoryString = '';
      break;
  }

  const rows = dataTable.getElementsByTagName('tr');
  for (let i = 0; i < rows.length; i++) {
    const row = rows[i];
    const productCell = row.cells[3];
    const categoryCell = row.cells[1];
    if ((categoryString === '' || categoryCell.innerText === categoryString) && productCell.innerText.toLowerCase().includes(searchText)) {
      row.style.display = '';
    } else {
      row.style.display = 'none';
    }
  }
}

/**
 * 현재 시간 설정 함수
 */
function setTime() {
  let today = new Date();
  let year = today.getFullYear();
  let month = today.getMonth() + 1;
  let date = today.getDate();
  todaySpan.innerHTML = `( ${year}년 ${month}월 ${date}일 )`;
}

/**
 * 메인 함수
 */
function main() {
  setTime();
  search();

  /**
   * 사용자가 필터를 선택하면, eventListener가 감지해서 상품 필터링 수행
   */
  userSelectedCategory.addEventListener('change', (event) => {
    const selectedCategory = event.target.value;
    filterData(selectedCategory);
  });

  /**
   * 사용자가 체크박스를 선택하고, 삭제 버튼을 누르는 event 발생 시, 체크된 row를 삭제
   */
  deleteButton.addEventListener('click', () => {
    const rows = dataTable.getElementsByTagName('tr');
    for (let i = rows.length - 1; i >= 0; i--) {
      const row = rows[i];
      const checkbox = row.getElementsByTagName('input')[0];
      if (checkbox && checkbox.checked) {
        dataTable.deleteRow(i);
      }
    }
  });
}

// js 실행
main();
