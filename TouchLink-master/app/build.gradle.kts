import org.jetbrains.kotlin.gradle.dsl.JvmTarget

plugins {
    alias(libs.plugins.agp.app)
    alias(libs.plugins.kotlin.android)
    alias(libs.plugins.hiddenapi.refine)
}

val cfgMinSdkVersion: Int by rootProject.extra
val cfgTargetSdkVersion: Int by rootProject.extra
val cfgCompileSdkVersion: Int by rootProject.extra
val cfgSourceCompatibility: JavaVersion by rootProject.extra
val cfgTargetCompatibility: JavaVersion by rootProject.extra
val cfgKotlinJvmTarget: JvmTarget by rootProject.extra

android {
    namespace = "xyz.mufanc.taa"
    compileSdk = cfgCompileSdkVersion

    defaultConfig {
        applicationId = "xyz.mufanc.taa"
        minSdk = cfgMinSdkVersion
        targetSdk = cfgTargetSdkVersion
        versionCode = 1
        versionName = "1.0"
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

kotlin {
    compilerOptions {
        jvmTarget.set(cfgKotlinJvmTarget)
    }
}

dependencies {
    compileOnly(project(":hiddenapi"))
    implementation(libs.core.ktx)
    implementation(libs.kotlinx.coroutines.core)
    implementation(libs.kotlinx.coroutines.android)
    implementation(libs.hiddenapi.runtime)
    implementation(libs.moshi.kotlin)
}

tasks.register("deployRelease") {
    group = "deployment"
    description = "Build and push release APK to device"

    dependsOn("assembleRelease")

    doLast {
        val outputApk = File(
            layout.buildDirectory.dir("outputs/apk/release").get().asFile,
            "app-release-unsigned.apk"
        )

        println("Found APK: ${outputApk.absolutePath}")
        println("Pushing to device...")

        val adb = android.adbExecutable.absolutePath

        val args = listOf(adb, "push", outputApk.absolutePath, "/data/local/tmp/touchlink.apk")
        val process = ProcessBuilder(args)
            .redirectOutput(ProcessBuilder.Redirect.INHERIT)
            .redirectError(ProcessBuilder.Redirect.INHERIT)
            .start()

        val code = process.waitFor()
        if (code != 0) {
            throw GradleException("Failed to push APK to device (exit code: $code)")
        }

        println("Successfully pushed APK to device")
    }
}
