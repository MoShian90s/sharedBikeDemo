<template id="main">
<el-row type="flex" justify="center" style="flex-wrap:wrap">
    <el-col class="InfoCards" :xs='24' :sm='24' :md='24' :lg='24' :xl='24'>

        <el-card class='box-card' ref="InfoCards" shadow='always' style="max-height: 100vh;transition:max-height 1s">
            <el-row type="flex" style="flex-wrap:wrap;justify-content:center">
                <el-col class="switcher" :xs='12' :sm='12' :md='6' :lg='6' :xl='6'>
                    <el-tooltip class="item" :open-delay='500' effect="dark" content="Search" placement="top-start">
                        <el-button icon="el-icon-search" circle @click.native="switchToSearch"></el-button>
                    </el-tooltip>
                </el-col>
                <el-col class="switcher" :xs='12' :sm='12' :md='6' :lg='6' :xl='6'>
                    <el-tooltip class="item" :open-delay='500' effect="dark" content="Delete" placement="top-start">
                        <el-button type="danger" icon="el-icon-delete" circle @click.native="switchToDelete"></el-button>
                    </el-tooltip>
                </el-col>
                <el-col class="switcher" :xs='12' :sm='12' :md='6' :lg='6' :xl='6'>
                    <el-tooltip class="item" :open-delay='500' effect="dark" content="Editor Mode" placement="top-start">
                        <el-button type="primary" icon="el-icon-edit" circle @click.native="switchToEdit"></el-button>
                    </el-tooltip>
                </el-col>
                <el-col class="switcher" :xs='12' :sm='12' :md='6' :lg='6' :xl='6'>
                    <el-tooltip class="item" :open-delay='500' effect="dark" content="Add" placement="top-start">
                        <el-button type="primary" icon="el-icon-circle-plus-outline" circle @click.native="switchToCreate"></el-button>
                    </el-tooltip>
                </el-col>
            </el-row>
        </el-card>

    </el-col>
    <el-col class="InfoCards" :xs='24' :sm='24' :md='24' :lg='24' :xl='24'>
        
        <transition name="frame" mode="out-in" enter-active-class="scale-in-center" leave-active-class="scale-out-center" :duration="{ enter: 300, leave: 300 }">
            <component :is="toolbarComponent" v-on:update="update" :newInfoMsg="newInfoMsg"></component>
        </transition>
        
    </el-col>
</el-row>
</template>

<script>
import Search from './TableToolbarComponents/Search'
import Edit from './TableToolbarComponents/Update'
import Delete from './TableToolbarComponents/Delete'
import Create from './TableToolbarComponents/Create'

export default {
    template:"#main",
    props:{
        newInfoMsg:Object,
    },
    data(){
        return{
            toolbarComponent:'Search',
        }
    },
    components:{
        Search,
        Edit,
        Delete,
        Create
    },
    methods:{
        switchToSearch(){
            this.toolbarComponent="Search"
        },
        switchToDelete(){
            this.toolbarComponent="Delete"
        },
        switchToEdit(){
            this.toolbarComponent="Edit"
        },
        switchToCreate(){
            this.toolbarComponent="Create"
        },
        update(){
            this.$emit("update","update")
        }
    }
}
</script>

<style scoped>

.InfoCards{
    margin-bottom: 5vh!important;
    transition:1s!important;
}
.scale-in-center {
	-webkit-animation: scale-in-center 0.3s cubic-bezier(0.250, 0.460, 0.450, 0.940) both;
	animation: scale-in-center 0.3s cubic-bezier(0.250, 0.460, 0.450, 0.940) both;
}
@-webkit-keyframes scale-in-center {
  0% {
    -webkit-transform: scale(0);
            transform: scale(0);
    opacity: 1;
  }
  100% {
    -webkit-transform: scale(1);
            transform: scale(1);
    opacity: 1;
  }
}
@keyframes scale-in-center {
  0% {
    -webkit-transform: scale(0);
            transform: scale(0);
    opacity: 1;
  }
  100% {
    -webkit-transform: scale(1);
            transform: scale(1);
    opacity: 1;
  }
}

.scale-out-center {
	-webkit-animation: scale-out-center 0.3s cubic-bezier(0.550, 0.085, 0.680, 0.530) both;
	animation: scale-out-center 0.3s cubic-bezier(0.550, 0.085, 0.680, 0.530) both;
}
@-webkit-keyframes scale-out-center {
  0% {
    -webkit-transform: scale(1);
            transform: scale(1);
    opacity: 1;
  }
  100% {
    -webkit-transform: scale(0);
            transform: scale(0);
    opacity: 1;
  }
}
@keyframes scale-out-center {
  0% {
    -webkit-transform: scale(1);
            transform: scale(1);
    opacity: 1;
  }
  100% {
    -webkit-transform: scale(0);
            transform: scale(0);
    opacity: 1;
  }
}

</style>