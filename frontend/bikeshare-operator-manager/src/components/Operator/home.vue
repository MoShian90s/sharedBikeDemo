<template>
  <el-container class="home_container">
    <el-header>
      <div>
        <img src="../../assets/bike.png" width="15%" height="15%" />
        <span>BikeShare for Operator</span>
      </div>
      <el-button style="background-color:#07689f;color: aliceblue;" @click="logout">logout</el-button>
    </el-header>
    <el-container>
      <el-aside :width="isCollapse ?'56px':'250px'">
        <div class="toggle-button" @click="toggleCollapse">|||</div>
        <el-menu background-color="#07689f" text-color="#fff" active-text-color="#a2d5f2" unique-opened :collapse="isCollapse"
          :collapse-transition="false" :router="true" default-active=$route.path>
          <el-submenu index="1">
            <template slot="title">
              <i class="el-icon-location" style="color:white;"></i>
              <span>Bike information</span>
            </template>
            <el-menu-item index="bikeMap">
              <template slot="title">
                <i class="el-icon-location" style="color:white;"></i>
                <span>Map</span>
              </template>
            </el-menu-item>
            <el-menu-item index="bikeSearch">
              <template slot="title">
                <i class="el-icon-document" style="color:white;"></i>
                <span>Search by information</span>
              </template>
            </el-menu-item>
            <el-menu-item index="bikeRegister">
              <template slot="title">
                <i class="el-icon-document" style="color:white;"></i>
                <span>Bike Register</span>
              </template>
            </el-menu-item>
          </el-submenu>
          <el-submenu index="2">
            <template slot="title">
              <i class="el-icon-menu" style="color:white;"></i>
              <span>Maintenance information</span>
            </template>
            <el-menu-item index="repairRequest">
              <template slot="title">
                <i class="el-icon-menu" style="color:white;"></i>
                <span>Repair request</span>
              </template>
            </el-menu-item>
            <el-menu-item index="repairOrder">
              <template slot="title">
                <i class="el-icon-document" style="color:white;"></i>
                <span>Your order</span>
              </template>
            </el-menu-item>
          </el-submenu>
          <el-submenu index="3">
            <template slot="title">
              <i class="el-icon-document" style="color:white;"></i>
              <span>Transport information</span>
            </template>
            <el-menu-item index="locationNumber">
              <template slot="title">
                <i class="el-icon-menu" style="color:white;"></i>
                <span>Location information</span>
              </template>
            </el-menu-item>
            <el-menu-item index="moveOrder">
              <template slot="title">
                <i class="el-icon-document" style="color:white;"></i>
                <span>Your order</span>
              </template>
            </el-menu-item>
          </el-submenu>
          <el-menu-item index="editInfo">
            <i class="el-icon-setting" style="color:white;"></i>
            <span slot="title">Edit profile</span>
          </el-menu-item>
        </el-menu>
      </el-aside>
      <el-main>
        <router-view>
        </router-view>
      </el-main>
    </el-container>
  </el-container>
</template>

<script>
  import qs from 'qs'
  export default {
    beforeCreate: function() {
      if (!this.$session.exists()) {
        this.$router.push('/')
        this.$notify.error({
          title: 'no log information registered',
          message: 'you need to log in first'
        })
      }
    },
    data() {
      return {
        isCollapse: false
      }
    },
    methods: {
      logout() {

        let that = this
        var data = qs.stringify({
          "username": this.$session.get("username"),
          "user_type": 'Operator'
        })
        this.$axios.post(this.$baseURL + '/signout/', data).then(function(res) {
          console.log(res)
          window.sessionStorage.clear()
          that.$notify.success({
            title: 'log out',
            message: 'you have successfully logged out',
          });
        }).catch(function(err) {
          console.log(err)
        })
        this.$router.push('/login')
      },
      toggleCollapse() {
        this.isCollapse = !this.isCollapse
      }
    }
  }
</script>

<style lang="less" scoped>
  .el-header {
    background-color: #a2d5f2;
    display: flex;
    justify-content: space-between;
    padding-left: 0;
    align-items: center;
    color: #fff;
    font-size: 20px;

    >div {
      display: flex;
      align-items: center;

      span {
        margin-left: 15px;
      }
    }
  }

  .el-aside {
    background-color: #07689f;

    .el-menu {
      border-right: none;
    }
  }

  .el-main {
    background-color: #ffffff;
  }

  .home_container {
    height: 100%;
  }

  .toggle-button {
    background-color: #0990d9;
    font-size: 10px;
    line-height: 24px;
    color: #fff;
    text-align: center;
    letter-spacing: 0.2em;
    cursor: pointer;
  }
  .el-card{
	box-shadow: 0 1px 1px rgba(0,0,0,0.15) !important;
}
</style>
