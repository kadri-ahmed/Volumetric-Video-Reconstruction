import ccmasterkernel
import ccmasterkernel.bindings as ccb
import os
import sys
import time

pointCloudsDirPath = 'D:\\vrmovie\\export_vrmovie_3body\\export'
projectDirPath = 'D:\\vrmovie\\narvis-repo\sample-ply-pointcloud'
cameras = [
    os.listdir(os.path.join(pointCloudsDirPath, "cn01")),
    os.listdir(os.path.join(pointCloudsDirPath, "cn02")),
    os.listdir(os.path.join(pointCloudsDirPath, "cn03")),
    os.listdir(os.path.join(pointCloudsDirPath, "cn04")),
    os.listdir(os.path.join(pointCloudsDirPath, "cn05")),
    os.listdir(os.path.join(pointCloudsDirPath, "cn06"))
]

def filter_cameras():
    for i in range(0,len(cameras)):
        cameras[i] = list(filter(lambda file: file.endswith(".e57"), cameras[i]))
        #take first 1761 point clouds
        while len(cameras[i]) > 1761:
            cameras[i].pop()
        cameras[i].reverse()
        while(len(cameras[i]) > 1761):
            cameras[i].pop()

def main():
    print('MasterKernel version %s' % ccmasterkernel.version())
    name = ccmasterkernel.ProductionDriverManager.getDriver(0).getShortName()
    print(name)

    if not ccmasterkernel.isLicenseValid():
        print("License error: ", ccmasterkernel.lastLicenseErrorMsg())
        sys.exit(0)
    # --------------------------------------------------------------------
    # create project
    # --------------------------------------------------------------------
    projectName = os.path.basename(projectDirPath)

    project = ccmasterkernel.Project()
    project.setName(projectName)
    project.setDescription('Automatically generate mesh from pointcloud')
    project.setProjectFilePath(os.path.join(projectDirPath, projectName))
    err = project.writeToFile()
    if not err.isNone():
        print(err.message)
        sys.exit(0)

    print('Project %s successfully created.' % projectName)
    print('')
    # --------------------------------------------------------------------
    # create block & import point cloud
    # --------------------------------------------------------------------
    for i in range(0,len(cameras[0])):
        block = ccmasterkernel.Block(project)
        project.addBlock(block)
        block.setName('block #%s' % (len(cameras[0])-i))
        block.setDescription('input point clouds')
        exportDestination = ""
        for cn0X in range(0,len(cameras)):
            file = cameras[cn0X].pop()
            exportDestination = file
            filepath = os.path.join(pointCloudsDirPath,"cn0%s" % (cn0X+1),os.fsdecode(file))
            importError = block.importPointCloud(filepath, "")
            if not importError.isNone():
                print(importError.message())
                sys.exit(0)
            print(file + " has been imported.")

        # --------------------------------------------------------------------
        # create reconstruction
        # --------------------------------------------------------------------    

        reconstruction = ccmasterkernel.Reconstruction(block)
        reconstruction_settings = reconstruction.getSettings()
        reconstruction_settings.geometrySimplificationToleranceinPixels = 0.025
        reconstruction_settings.geometrySimplificationMode = ccb.GeometrySimplificationMode.GeometrySimplification_planar
        reconstruction.setSettings(reconstruction_settings)
        block.addReconstruction(reconstruction)
        if reconstruction.getNumInternalTiles() == 0:
            print('Error: Failed to create reconstruction layout.')
            sys.exit(0)

        # --------------------------------------------------------------------
        # Production
        # --------------------------------------------------------------------
        production = ccmasterkernel.Production(reconstruction)
        reconstruction.addProduction(production)
        production.setDriverName('OBJ') # specify export format [FBX, OBJ,...]
        production.setDestination(os.path.join(project.getProductionsDirPath(), exportDestination))

        driverOptions = production.getDriverOptions()
        # (optional) specify some options
        production.setDriverOptions(driverOptions)
        print('Production item created.')

        productionSubmitError = production.submitProcessing()

        if not productionSubmitError.isNone():
            print('Error: Failed to submit production.')
            print(productionSubmitError.message)
            sys.exit(0)

        print('The production job has been submitted and is waiting to be processed...')

        iPreviousProgress = 0
        iProgress = 0
        previousJobStatus = ccmasterkernel.JobStatus.Job_unknown

        while 1:
            jobStatus = production.getJobStatus()

            if jobStatus != previousJobStatus:
                print(ccmasterkernel.jobStatusAsString(jobStatus))

            if jobStatus == ccmasterkernel.JobStatus.Job_failed or jobStatus == ccmasterkernel.JobStatus.Job_cancelled or jobStatus == ccmasterkernel.JobStatus.Job_completed:
                break

            if iProgress != iPreviousProgress:
                print('%s%% - %s' % (iProgress, production.getJobMessage()))

            iPreviousProgress = iProgress
            iProgress = production.getJobProgress()
            time.sleep(1)
            production.updateJobStatus()
            previousJobStatus = jobStatus

        print('')

        if jobStatus != ccmasterkernel.JobStatus.Job_completed:
            print('"Error: Incomplete production')

            if production.getJobMessage() != '':
                print(production.getJobMessage())


if __name__ == '__main__':
    filter_cameras()
    main()
