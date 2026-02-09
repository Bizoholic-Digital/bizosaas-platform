export type Platform = 'bizosaas' | 'thrillring' | 'bizoholic'

export const platformConfig = {
    name: "Thrillring Gaming",
    theme: {
        primaryColor: "#000000",
        logo: "/logo.png",
        className: "platform-thrillring"
    },
    features: {
        multiTenant: true,
        customBranding: true
    }
};

export const getCurrentPlatform = (): Platform => 'thrillring';
export const getPlatformConfig = (platform: Platform = 'thrillring') => platformConfig;
export const getPlatformMetadata = () => ({ title: platformConfig.name });
export const getPlatformClassName = () => "thrillring-theme";
export default platformConfig;
