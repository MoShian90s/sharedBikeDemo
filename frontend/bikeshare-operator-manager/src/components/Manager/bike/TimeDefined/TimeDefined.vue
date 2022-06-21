<template>
<div>
    <charts></charts>
    <el-divider class="divider"><i class="el-icon-sort"></i></el-divider>
    <Map></Map>
</div>
</template>

<script>
import Charts from './Charts'
import Map from './Map'

export default {
    components:{
        Charts,
        Map,
    }
}
</script>

<style scoped>
.divider{
    margin: 7vh 0 7vh 0;
}
</style>