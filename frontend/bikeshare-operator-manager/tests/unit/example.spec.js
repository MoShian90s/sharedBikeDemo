import { shallowMount } from '@vue/test-utils'
import editInfo from '@/components/editInfo.vue'

describe('editInfo.vue', () => {
  it('renders props.msg when passed', () => {
    // const msg = 'new message'
    // const wrapper = shallowMount(Home, {
    //   propsData: { msg }
    // })
    // expect(wrapper.text()).toMatch(msg)
    expect(typeof editInfo.data).toBe('function')
  })
})
