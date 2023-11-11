<template>
  <div class="sidebar"></div>
</template>

<style>
.sidebar {
  border-top-right-radius: 30px;
  background-color: #d9d9d9;
  position: fixed;
  bottom: 0;
  left: 0;
  background: rgba(217, 217, 217, 0.5);
}

@media (min-width: 1000px) {
  .sidebar {
    width: 340px;
    height: 76vh;
  }
}

@media (max-width: 1001px) {
  .sidebar {
    display: none;
  }
}
</style>