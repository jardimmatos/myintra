import ConfigService from '../index'
class WikiService extends ConfigService {
    constructor(){
        super('wiki/api/v1/')
    }
}
export default WikiService
