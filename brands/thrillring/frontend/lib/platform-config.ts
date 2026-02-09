import { platformConfig as mainConfig, getCurrentPlatform } from './platform';

export const platformConfig = mainConfig;

export const usePlatform = () => {
    return {
        platform: getCurrentPlatform(),
        config: mainConfig
    };
};

export default platformConfig;
