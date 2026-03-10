import org.jetbrains.kotlin.gradle.dsl.JvmTarget

plugins {
    alias(libs.plugins.agp.app) apply false
    alias(libs.plugins.agp.lib) apply false
    alias(libs.plugins.kotlin.android) apply false
}

val cfgMinSdkVersion by extra(30)
val cfgTargetSdkVersion by extra(36)
val cfgCompileSdkVersion by extra(36)
val cfgSourceCompatibility by extra(JavaVersion.VERSION_17)
val cfgTargetCompatibility by extra(JavaVersion.VERSION_17)
val cfgKotlinJvmTarget by extra(JvmTarget.JVM_17)
