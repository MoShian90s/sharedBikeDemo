<template>
<div id="app">
	<transition mode="out-in" enter-active-class="slide-in-top" leave-active-class="slide-out-top" :duration="{enter: 300, leave: 300 }">
		<router-view></router-view>
	</transition>
</div>
</template>

<style>
	body{
		margin:0;
	}
	html::-webkit-scrollbar {
		width:0;
	}
	::-webkit-scrollbar{
		width: 1px;
		background-color: transparent;
	}
</style>
<style scoped>
	#app{
		background:#ffffff;
	}
	/* all code blocks below are animation class css */
	.slide-in-top {
		-webkit-animation: slide-in-top 0.3s cubic-bezier(0.250, 0.460, 0.450, 0.940) both;
				animation: slide-in-top 0.3s cubic-bezier(0.250, 0.460, 0.450, 0.940) both;
	}

	/**
	* ----------------------------------------
	* animation slide-in-top
	* ----------------------------------------
	*/
	@-webkit-keyframes slide-in-top {
		0% {
			-webkit-transform: translateY(-1000px);
					transform: translateY(-1000px);
			opacity: 0;
		}
		100% {
			-webkit-transform: translateY(0);
					transform: translateY(0);
			opacity: 1;
		}
	}
	@keyframes slide-in-top {
	0% {
		-webkit-transform: translateY(-1000px);
				transform: translateY(-1000px);
		opacity: 0;
	}
	100% {
		-webkit-transform: translateY(0);
				transform: translateY(0);
		opacity: 1;
	}
	}

	.slide-out-top {
		-webkit-animation: slide-out-top 0.3s cubic-bezier(0.550, 0.085, 0.680, 0.530) both;
				animation: slide-out-top 0.3s cubic-bezier(0.550, 0.085, 0.680, 0.530) both;
	}

	/**
	* ----------------------------------------
	* animation slide-out-top
	* ----------------------------------------
	*/
	@-webkit-keyframes slide-out-top {
		0% {
			-webkit-transform: translateY(0);
					transform: translateY(0);
			opacity: 1;
		}
		100% {
			-webkit-transform: translateY(-1000px);
					transform: translateY(-1000px);
			opacity: 0;
		}
	}
	@keyframes slide-out-top {
		0% {
			-webkit-transform: translateY(0);
					transform: translateY(0);
			opacity: 1;
		}
		100% {
			-webkit-transform: translateY(-1000px);
					transform: translateY(-1000px);
			opacity: 0;
		}
	}
</style>
