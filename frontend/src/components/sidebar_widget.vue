<template>
  <div class="sidebar"></div>
</template>

<style>
.sidebar {
  border-top-right-radius: 30px;
  position: fixed;
  bottom: 0;
  left: 0;
  background: rgba(217, 217, 217, 0.2);
  z-index: 1; 
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