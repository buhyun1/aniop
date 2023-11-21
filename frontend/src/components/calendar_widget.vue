<template>
  <div class="wrapper">
    <header>
        <div class="nav">
          <span class="arrow-prev"></span>
          <p class="current-date">September 2022</p>
          <span class="arrow-next"></span>
        </div>
      </header>
      <div class="calendar">
        <ul class="weeks">
          <li>Sun</li>
          <li>Mon</li>
          <li>Tue</li>
          <li>Wed</li>
          <li>Thu</li>
          <li>Fri</li>
          <li>Sat</li>
        </ul>
        <ul class="days">
          <li class="inactive">27</li>
          <li class="inactive">28</li>
          <li class="inactive">29</li>
          <li class="inactive">30</li>
          <li>1</li>
          <li>2</li>
          <li>3</li>
          <li>4</li>
          <li>5</li>
          <li>6</li>
          <li>7</li>
          <li>8</li>
          <li>9</li>
          <li>10</li>
          <li>11</li>
          <li>12</li>
          <li>13</li>
          <li>14</li>
          <li>15</li>
          <li>16</li>
          <li>17</li>
          <li>18</li>
          <li>19</li>
          <li>20</li>
          <li>21</li>
          <li>22</li>
          <li>23</li>
          <li>24</li>
          <li>25</li>
          <li>26</li>
          <li>27</li>
          <li>28</li>
          <li>29</li>
          <li>30</li>
          <li>31</li>
        </ul>
      </div>
    </div>
</template>

<script>

</script>

<style>
	@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@400;500;600&display=swap');
 
 /*#2 */
* {
  margin: 0;
  padding: 0;
  box-sizing: border-box;
  font-family: 'Poppins', sans-serif;
}
 .arrow-prev,
.arrow-next {
    position: relative;
    float:left;
    width:100px;
    height:100px;
    margin-right:5px;
}

.arrow-prev::after {
    position: absolute;
    left: 25px; 
    top: 20px;
    content: '';
    width: 25px; /* 사이즈 */
    height: 25px; /* 사이즈 */
    border-top: 5px solid #000; /* 선 두께 */
    border-right: 5px solid #000; /* 선 두께 */
    transform: rotate(225deg); /* 각도 */
}

.arrow-next::after {
    position: absolute;
    left: 20px; 
    top: 20px; 
    content: '';
    width: 25px; /* 사이즈 */
    height: 25px; /* 사이즈 */
    border-top: 5px solid #000; /* 선 두께 */
    border-right: 5px solid #000; /* 선 두께 */
    transform: rotate(45deg); /* 각도 */
}
 /*#3 */
button {
  /* button 요소에 기본적으로 설정되는 스타일 속성 초기화 */
  border: none;
  outline: none;
  background-color: transparent;
  padding: 0;
  cursor: pointer;
}
 
 /*#4 */
body {
  display: flex;
  align-items: center;
  justify-content: center;
  min-height: 100vh;
}

	.wrapper {
  width: 450px;
  background: #fff;
  border-radius: 10px;
  padding: 25px;
}
 
/*#6*/
.wrapper .nav {
  display: flex;
  align-items: center;
  justify-content: space-between;
  margin-bottom: 30px;
}
.wrapper .nav .current-date {
  font-size: 23px;
  font-weight: 600;
}
.wrapper .nav button {
  width: 38px;
  height: 38px;
  font-size: 30px;
  color: #878787;
}
	/*#7*/
.calendar ul {
  display: flex;
  list-style: none;
  flex-wrap: wrap;
  text-align: center;
}
.calendar .weeks li {
  font-weight: 500;
}
.calendar .days {
  margin-bottom: 20px;
}
.calendar ul li {
  /*#8*/
  width: calc(100% / 7);
  /*#9*/
  position: relative;
}
.calendar .days li {
  /*#10*/
  z-index: 1;
  margin-top: 30px;
  cursor: pointer;
}
 
/*#11*/
.days li.inactive {
  color: #aaa;
}
.days li.active {
  color: #fff;
}
.calendar .days li::before {
  position: absolute;
  content: '';
  height: 40px;
  width: 40px;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  border-radius: 50%;
  z-index: -1;
}
.days li:hover::before {
  background: #f2f2f2;
}
.days li.active::before {
  background: #008aff;
}
</style>