plugins {
    alias(libs.plugins.agp.lib)
}

val cfgMinSdkVersion: Int by rootProject.extra
val cfgCompileSdkVersion: Int by rootProject.extra
val cfgSourceCompatibility: JavaVersion by rootProject.extra
val cfgTargetCompatibility: JavaVersion by rootProject.extra

android {
    namespace = "hidden.api.stub"
    compileSdk = cfgCompileSdkVersion

    defaultConfig {
        minSdk = cfgMinSdkVersion
        consumerProguardFiles("consumer-rules.pro")
    }

    buildTypes {
        release {
            isMinifyEnabled = false
            proguardFiles("proguard-rules.pro")
        }
    }

    compileOptions {
        sourceCompatibility = cfgSourceCompatibility
        targetCompatibility = cfgTargetCompatibility
    }
}

dependencies {
    compileOnly(libs.hiddenapi.annotation)
    annotationProcessor(libs.hiddenapi.processor)
}