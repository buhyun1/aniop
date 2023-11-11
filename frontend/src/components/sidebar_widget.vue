<template>
    <div class = "sidebar">
    </div>
</template>

<style>
    .sidebar{
        border-top-right-radius: 30px;
        background-color: #D9D9D9;
        position: fixed;
        bottom: 0;
        left: 0;
        background: rgba(217, 217, 217, 0.5);;
    }

    @media (min-width: 768px) {
        .sidebar {
            width: 340px;
            height: 80vh;
        }
    }

    @media (max-width: 767px) {
        .sidebar {
            width: 240px; 
            height: 60vh; 
        }
    }
</style>