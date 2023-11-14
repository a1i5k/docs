// ===============================================================================
//						  NVIDIA PHYSX SDK TRAINING PROGRAMS
//						   LESSON 116: RIGIDBODY FORCEFIELD
//
//						    Written by QA BJ, 6-2-2008
// ===============================================================================

#include "Lesson116.h"
#include "Timing.h"
#include <climits>
#include <iostream>
#include <vector>
#include <functional>
#include <queue>
#include <ctime>
#include <math.h>
#include <time.h>
#include <fstream>
using namespace std;
NxVec3 getColor(int _color);
void GenerateGraph(std::vector<NxVec3>& points, std::vector< std::vector<int> >& ribs, int N, int M);
void DrawGraph(std::vector<NxVec3> points, std::vector< std::vector<int> > ribs);
float dc(float d);
void GetGraphMatrix(std::vector<NxVec3>& points, std::vector< std::vector<int> >& ribs);
std::vector<int> path(int start, int end);
void painted(std::vector<int> path, int color);
std::vector<NxVec3> points;
std::vector< std::vector<int> > ribs;
std::vector< std::vector<double> > matrix;
int graphPointsCountX = 7;
int graphPointsCountY = 7;
int objectsCount = 7;
float offsetX = 0.3;
float offsetY = 0.3;
float offsetZ = 0.3;
float objectVelocity = 0.75;
class Ball {
public:
	float start = getCurrentTime();
	Ball(NxActor* _body) {
		body = _body;
		color = 0;
	}
	void setPath(std::vector<int> _path) {
		bpath = _path;
	}
	void setColor(int _color) {
		color = _color;
	}
	void print_white() {
		if (!bpath.empty()) {
			NxVec3 p1 = points[bpath[bpath.size() - 1]];
			NxVec3 p2 = points[bpath[bpath.size() - 2]];
			NxVec3 lastPos = body->getGlobalPosition();
			NxVec3 newPos;
			NxVec3 colorForArrow(0, 1, 1);
			for (int i = 0; i < (bpath.size() - 2); i++) {
				DrawArrow(points[bpath[i + 1]], points[bpath[i]],
					getColor(color));
				;
			}
			start = getCurrentTime();
		}
	}
	void print() {
		if (!bpath.empty()) {
			NxVec3 p1 = points[bpath[bpath.size() - 1]];
			NxVec3 p2 = points[bpath[bpath.size() - 2]];
			NxVec3 lastPos = body->getGlobalPosition();
			NxVec3 newPos;
			NxVec3 colorForArrow(0, 1, 1);
			DrawArrow(body->getGlobalPosition(), p2, getColor(color));
			DrawLine(p1, body->getGlobalPosition(), getColor(273), 3.0f);
			start = getCurrentTime();
		}
	}
	void move() {
		if (!bpath.empty()) {
			NxVec3 p1 = points[bpath[bpath.size() - 1]];
			NxVec3 p2 = points[bpath[bpath.size() - 2]];
			NxVec3 lastPos = body->getGlobalPosition();
			NxVec3 newPos;
			NxVec3 colorForArrow(0, 1, 1);
			float end = getCurrentTime();
			float deltaTime = end - start;
			float lengh = sqrt((p2.x - p1.x) * (p2.x - p1.x) + (p2.y - p1.y) * (p2.y
				- p1.y) + (p2.z - p1.z) * (p2.z - p1.z));
			float alpha = acos((p2.x - p1.x) / lengh);
			float betta = acos((p2.y - p1.y) / lengh);
			float gamma = acos((p2.z - p1.z) / lengh);
			bool xb = p2.x > p1.x;
			bool yb = p2.y > p1.y;
			bool zb = p2.z > p1.z;
			if (xb && (lastPos.x > p2.x || lastPos.x < p1.x) || !xb && (lastPos.x
			> p1.x || lastPos.x < p2.x)
				&&
				yb && (lastPos.y > p2.y || lastPos.y < p1.y) || !yb &&
				(lastPos.y > p1.y || lastPos.y < p2.y)
				&&
				zb && (lastPos.z > p2.z || lastPos.z < p1.z) || !zb &&
				(lastPos.z > p1.z || lastPos.z < p2.z))
			{
				newPos = p2;
				int index1 = bpath[bpath.size() - 1];
				int index2 = bpath[bpath.size() - 2];
				bpath.pop_back();
				for (int j = 0; j < (int)ribs.size(); ++j) {
					if ((ribs[j])[0] == index1 && (ribs[j])[1] == index2
						|| (ribs[j])[1] == index1 && (ribs[j])[0] ==
						index2) {
						(ribs[j])[2] -= color;
					}
				}
				if (bpath.size() < 2) {
					int endVertex = rand() % points.size();
					while (bpath[0] == endVertex) endVertex = rand() %
						points.size();
					setPath(path(bpath[0], endVertex));
					painted(bpath, color);
				}
			}
			else {
				newPos = NxVec3(lastPos.x +
					cos(alpha) * objectVelocity * deltaTime,
					lastPos.y + cos(betta) * objectVelocity * deltaTime,
					lastPos.z + cos(gamma) * objectVelocity * deltaTime);
			}
			body->setGlobalPosition(newPos);
			start = getCurrentTime();
		}
	}
private:
	NxActor* body;
	int color;
	std::vector<int> bpath;
};
std::vector<Ball> balls;
// Physics SDK globals
NxPhysicsSDK* gPhysicsSDK = NULL;
NxScene* gScene = NULL;
NxVec3 gDefaultGravity(0, -9.8, 0);
// User report globals
DebugRenderer gDebugRenderer;
// HUD globals
HUD hud;
// Display globals
int gMainHandle;
int mx = 0;
int my = 0;
// Camera globals
float gCameraAspectRatio = 1.0f;
NxVec3 gCameraPos(0, 5, -15);
NxVec3 gCameraForward(0, 0, 1);
NxVec3 gCameraRight(-1, 0, 0);
const NxReal gCameraSpeed = 10;
// Force globals
NxVec3 gForceVec(0, 0, 0);
NxReal gForceStrength = 20000;
bool bForceMode = true;
// Keyboard globals
#define MAX_KEYS 256
bool gKeys[MAX_KEYS];
// Simulation globals
NxReal gDeltaTime = 1.0 / 60.0;
bool bHardwareScene = false;
bool bPause = false;
bool bShadows = false;
bool bDebugWireframeMode = false;
// Actor globals
NxActor* groundPlane = NULL;
// Focus actor
NxActor* gSelectedActor = NULL;
void PrintControls()
{
	printf("\n Flight Controls:\n ----------------\n w = forward, s = back\n a = strafe left, d = strafe right\n q = up, z = down\n");
}
void ProcessCameraKeys()
{
	NxReal deltaTime;
	if (bPause)
	{
		deltaTime = 0.0005;
	}
	else
	{
		deltaTime = gDeltaTime;
	}
	// Process camera keys
	for (int i = 0; i < MAX_KEYS; i++)
	{
		if (!gKeys[i]) { continue; }
		switch (i)
		{
			// Camera controls
		case 'w': { gCameraPos += gCameraForward * gCameraSpeed * deltaTime; break; }
		case 's': { gCameraPos -= gCameraForward * gCameraSpeed * deltaTime; break; }
		case 'a': { gCameraPos -= gCameraRight * gCameraSpeed * deltaTime; break; }
		case 'd': { gCameraPos += gCameraRight * gCameraSpeed * deltaTime; break; }
		case 'z': { gCameraPos -= NxVec3(0, 1, 0) * gCameraSpeed * deltaTime; break; }
		case 'q': { gCameraPos += NxVec3(0, 1, 0) * gCameraSpeed * deltaTime; break; }
		}
	}
}
void SetupCamera()
{
	gCameraAspectRatio = (float)glutGet(GLUT_WINDOW_WIDTH) /
		(float)glutGet(GLUT_WINDOW_HEIGHT);
	// Setup camera
	glMatrixMode(GL_PROJECTION);
	glLoadIdentity();
	gluPerspective(60.0f, gCameraAspectRatio, 1.0f, 10000.0f);
	gluLookAt(gCameraPos.x, gCameraPos.y, gCameraPos.z, gCameraPos.x +
		gCameraForward.x, gCameraPos.y + gCameraForward.y, gCameraPos.z + gCameraForward.z, 0.0f,
		1.0f, 0.0f);
	glMatrixMode(GL_MODELVIEW);
	glLoadIdentity();
}
void RenderActors(bool shadows)
{
	// Render all the actors in the scene
	NxU32 nbActors = gScene->getNbActors();
	NxActor** actors = gScene->getActors();
	while (nbActors--)
	{
		NxActor* actor = *actors++;
		DrawActor(actor, gSelectedActor, false);
		// Handle shadows
		if (shadows)
		{
			DrawActorShadow(actor, false);
		}
	}
	for (int i = 0; i < (int)balls.size(); ++i) {
		balls[i].move();
	}
	for (int i = 0; i < (int)balls.size(); ++i) {
		balls[i].print_white();
	}
	for (int i = 0; i < (int)balls.size(); ++i) {
		balls[i].print();
	}
}
void DrawForce(NxActor* actor, NxVec3& forceVec, const NxVec3& color)
{
	// Draw only if the force is large enough
	NxReal force = forceVec.magnitude();
	if (force < 0.1) return;
	forceVec = 1 * forceVec / force;
	NxVec3 pos = actor->getGlobalPosition();
	DrawArrow(pos, pos + forceVec, color);
}
bool IsSelectable(NxActor* actor)
{
	NxShape* const* shapes = gSelectedActor->getShapes();
	NxU32 nShapes = gSelectedActor->getNbShapes();
	while (nShapes--)
	{
		if (shapes[nShapes]->getFlag(NX_TRIGGER_ENABLE))
		{
			return false;
		}
	}
	if (!actor->isDynamic())
		return false;
	if (actor == groundPlane)
		return false;
	return true;
}
void SelectNextActor()
{
	NxU32 nbActors = gScene->getNbActors();
	NxActor** actors = gScene->getActors();
	for (NxU32 i = 0; i < nbActors; i++)
	{
		if (actors[i] == gSelectedActor)
		{
			NxU32 j = 1;
			gSelectedActor = actors[(i + j) % nbActors];
			while (!IsSelectable(gSelectedActor))
			{
				j++;
				gSelectedActor = actors[(i + j) % nbActors];
			}
			break;
		}
	}
}
void ProcessForceKeys()
{
	;
}
void ProcessInputs()
{
	ProcessForceKeys();
	// Show debug wireframes
	if (bDebugWireframeMode)
	{
		if (gScene) gDebugRenderer.renderData(*gScene->getDebugRenderable());
	}
}
void RenderCallback()
{
	// Clear buffers
	glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT);
	ProcessCameraKeys();
	SetupCamera();
	if (gScene && !bPause)
	{
		GetPhysicsResults();
		ProcessInputs();
		StartPhysics();
	}
	// Display scene
	RenderActors(bShadows);
	DrawForce(gSelectedActor, gForceVec, NxVec3(1, 1, 0));
	gForceVec = NxVec3(0, 0, 0);
	DrawGraph(points, ribs);
	// Render the HUD
	hud.Render();
	glFlush();
	glutSwapBuffers();
}
void ReshapeCallback(int width, int height)
{
	glViewport(0, 0, width, height);
	gCameraAspectRatio = float(width) / float(height);
}
void IdleCallback()
{
	glutPostRedisplay();
}
void KeyboardCallback(unsigned char key, int x, int y)
{
	gKeys[key] = true;
	switch (key)
	{
	default: { break; }
	}
}
void KeyboardUpCallback(unsigned char key, int x, int y)
{
	gKeys[key] = false;
	switch (key)
	{
	case 27: { exit(0); break; }
	default: { break; }
	}
}
void SpecialCallback(int key, int x, int y)
{
	switch (key)
	{
		// Reset PhysX
	case GLUT_KEY_F10: ResetNx(); return;
	}
}
void MouseCallback(int button, int state, int x, int y)
{
	mx = x;
	my = y;
}
void MotionCallback(int x, int y)
{
	int dx = mx - x;
	int dy = my - y;
	gCameraForward.normalize();
	gCameraRight.cross(gCameraForward, NxVec3(0, 1, 0));
	NxQuat qx(NxPiF32 * dx * 20 / 180.0f, NxVec3(0, 1, 0));
	qx.rotate(gCameraForward);
	NxQuat qy(NxPiF32 * dy * 20 / 180.0f, gCameraRight);
	qy.rotate(gCameraForward);
	mx = x;
	my = y;
}
void ExitCallback()
{
	ReleaseNx();
}
void InitGlut(int argc, char** argv)
{
	glutInit(&argc, argv);
	glutInitWindowSize(1024, 1024);
	glutInitDisplayMode(GLUT_RGB | GLUT_DOUBLE | GLUT_DEPTH);
	gMainHandle = glutCreateWindow("Lesson 101: Primary Shape");
	glutSetWindow(gMainHandle);
	glutDisplayFunc(RenderCallback);
	glutReshapeFunc(ReshapeCallback);
	glutIdleFunc(IdleCallback);
	glutKeyboardFunc(KeyboardCallback);
	glutKeyboardUpFunc(KeyboardUpCallback);
	glutSpecialFunc(SpecialCallback);
	glutMouseFunc(MouseCallback);
	glutMotionFunc(MotionCallback);
	MotionCallback(0, 0);
	atexit(ExitCallback);
	// Setup default render states
	glClearColor(0.0f, 0.0f, 0.0f, 1.0f);
	glEnable(GL_DEPTH_TEST);
	glEnable(GL_COLOR_MATERIAL);
	glEnable(GL_CULL_FACE);
	// Setup lighting
	glEnable(GL_LIGHTING);
	float AmbientColor[] = { 0.0f, 0.1f, 0.2f, 0.0f }; glLightfv(GL_LIGHT0,
		GL_AMBIENT, AmbientColor);
	float DiffuseColor[] = { 0.2f, 0.2f, 0.2f, 0.0f }; glLightfv(GL_LIGHT0,
		GL_DIFFUSE, DiffuseColor);
	float SpecularColor[] = { 0.5f, 0.5f, 0.5f, 0.0f }; glLightfv(GL_LIGHT0,
		GL_SPECULAR, SpecularColor);
	float Position[] = { 100.0f, 100.0f, -400.0f, 1.0f }; glLightfv(GL_LIGHT0,
		GL_POSITION, Position);
	glEnable(GL_LIGHT0);
}
NxActor* CreateGroundPlane()
{
	// Create a plane with default descriptor
	NxPlaneShapeDesc planeDesc;
	NxActorDesc actorDesc;
	actorDesc.shapes.pushBack(&planeDesc);
	return gScene->createActor(actorDesc);
}
NxActor* CreateSphere(int vertexIndex) {
	// Add a single-shape actor to the scene
	NxActorDesc actorDesc;
	NxBodyDesc bodyDesc;
	// The actor has one shape, a sphere, 1m on radius
	NxSphereShapeDesc sphereDesc;
	sphereDesc.radius = 0.05f;
	sphereDesc.localPose.t = NxVec3(0, 0, 0);
	actorDesc.shapes.pushBack(&sphereDesc);
	actorDesc.density = 10.0f;
	actorDesc.globalPose.t = points[vertexIndex];
	return gScene->createActor(actorDesc);
}
void InitializeHUD()
{
	bHardwareScene = (gScene->getSimType() == NX_SIMULATION_HW);
	hud.Clear();
	// Add pause to HUD
	if (bPause)
		hud.AddDisplayString("Paused - Hit \"p\" to Unpause", 0.3f, 0.55f);
	else
		hud.AddDisplayString("", 0.0f, 0.0f);
}
void InitNx()
{
	std::ofstream fout("C:\\Users\\hp\\Desktop\\graph.csv", std::ofstream::app);
	// Initialize camera parameters
	gCameraAspectRatio = 1.0f;
	gCameraPos = NxVec3(3, 10, -10);
	gCameraForward = NxVec3(0, 0, 1);
	gCameraRight = NxVec3(-1, 0, 0);
	// Create the physics SDK
	gPhysicsSDK = NxCreatePhysicsSDK(NX_PHYSICS_SDK_VERSION);
	if (!gPhysicsSDK) return;
	// Set the physics parameters
	gPhysicsSDK->setParameter(NX_SKIN_WIDTH, 0.01);
	// Set the debug visualization parameters
	gPhysicsSDK->setParameter(NX_VISUALIZATION_SCALE, 1);
	gPhysicsSDK->setParameter(NX_VISUALIZE_COLLISION_SHAPES, 1);
	gPhysicsSDK->setParameter(NX_VISUALIZE_ACTOR_AXES, 1);
	// Create the scene
	NxSceneDesc sceneDesc;
	sceneDesc.simType = NX_SIMULATION_SW;
	sceneDesc.gravity = gDefaultGravity;
	gScene = gPhysicsSDK->createScene(sceneDesc);
	if (!gScene)
	{
		sceneDesc.simType = NX_SIMULATION_SW;
		gScene = gPhysicsSDK->createScene(sceneDesc);
		if (!gScene) return;
	}
	// Create the default material
	NxMaterial* defaultMaterial = gScene->getMaterialFromIndex(0);
	defaultMaterial->setRestitution(0.5);
	defaultMaterial->setStaticFriction(0.5);
	defaultMaterial->setDynamicFriction(0.5);
	// Create the objects in the scene
	groundPlane = CreateGroundPlane();
	int colorCounter = 0;
	int nextColor;
	int flag = 0;
	int unic[4][4][4];
	for (int i = 0; i < 4; i++)
	{
		for (int j = 0; j < 4; j++)
		{
			for (int k = 0; k < 4; k++)
			{
				unic[i][j][k] = 0;
			}
		}
	}
	unic[0][0][0] = 1;
	if (objectsCount > 42) objectsCount = 42;
	int a = 0;
	int b = 4;
	int N = objectsCount; 
	for (int i = 0; i < objectsCount; ++i) {
		int startVertex = rand() % points.size();
		int endVertex = rand() % points.size();
		while (startVertex == endVertex) endVertex = rand() % points.size();
		Ball temp = Ball(CreateSphere(startVertex));

		int x, y, z;
		flag = 0;
		while (flag == 0)
		{
			x = a + (b - a) * ((rand() % 999) * 0.001);
			y = a + (b - a) * ((rand() % 999) * 0.001);
			z = a + (b - a) * ((rand() % 999) * 0.001);
			if (unic[x][y][z] == 0)
			{
				nextColor = pow(2, x) + pow(2, y) * 16 + pow(2, z) * 256;
				flag = 1;
				unic[x][y][z] = 1;
			}
		}
		int color = nextColor;
		fout << x << ", " << y << ", " << z << std::endl;
		auto tempPath = path(startVertex, endVertex);
		temp.setPath(tempPath);
		temp.setColor(color);
		painted(tempPath, color);
		balls.push_back(temp);
	}
	// Initialize HUD
	InitializeHUD();
	// Get the current time
	getElapsedTime();
	// Start the first frame of the simulation
	if (gScene) StartPhysics();
	fout.close();
}
void ReleaseNx()
{
	if (gScene)
	{
		GetPhysicsResults();
		gPhysicsSDK->releaseScene(*gScene);
	}
	if (gPhysicsSDK) gPhysicsSDK->release();
}
void ResetNx()
{
	ReleaseNx();
	InitNx();
}
void StartPhysics()
{
	gDeltaTime = getElapsedTime();
	gScene->simulate(gDeltaTime);
	gScene->flushStream();
}
void GetPhysicsResults()
{
	while (!gScene->fetchResults(NX_RIGID_BODY_FINISHED, false));
}
int eightBits(int& source) {
	int result = 0;
	for (int i = 0; i < 4; ++i) {
		result += source & 1;
		result <<= 1;
		source >>= 1;
	}
	return result;
}
float getColorLayer(int& n) {
	return (float)eightBits(n) / 16.0;
}
NxVec3 getColor(int _color) {
	return NxVec3(getColorLayer(_color), getColorLayer(_color),
		getColorLayer(_color));
}
void DrawGraph(std::vector<NxVec3> points, std::vector< std::vector<int> > ribs) {
	for (int i = 0; i < (int)ribs.size(); ++i) {
		int p1 = (ribs[i])[0];
		int p2 = (ribs[i])[1];
		int color = (ribs[i])[2];
		if (color == 273)
			DrawLine(points[p1], points[p2], getColor(color), 3.0f);
	}
}
double random(double min, double max)
{
	return (double)(rand()) / RAND_MAX * (max - min) + min;
}
float dc(float d) {
	return random(0, d) * (rand() % 2 == 0 ? -1 : 1);
}
void GenerateGraph(std::vector<NxVec3>& points, std::vector< std::vector<int> >& ribs, int graphPointsCountX, int graphPointsCountY) {
	int countVert = 0;
	if (graphPointsCountX < 2) return;
	for (int i = 0; i < graphPointsCountX; ++i) {
		for (int j = 0; j < graphPointsCountY; ++j) {
			float randX = dc(offsetX);
			float randZ = dc(offsetZ);
			float randY = dc(offsetY);
			points.push_back(NxVec3(1.0f * j + randX, offsetZ * 2 + randZ, 1.0f *
				i + randY));
		}
	}
	int color = 273;
	for (int i = 0; i < graphPointsCountX - 1; ++i) {
		for (int j = 0; j < graphPointsCountY - 1; ++j) {
			std::vector<int> temp;
			temp.push_back(graphPointsCountY * i + j);
			temp.push_back(graphPointsCountY * i + j + 1);
			temp.push_back(color);
			int temp1, temp2;
			if (temp1 = (rand() % 12)) ribs.push_back(temp);
			temp.clear();
			temp.push_back(graphPointsCountY * i + j);
			temp.push_back(graphPointsCountY * i + j + graphPointsCountY);
			cout << "connecting " << graphPointsCountY * i + j << " with " << graphPointsCountY + j + graphPointsCountY << endl;
			temp.push_back(color);
			if ((temp2 = (rand() % 4)) || !temp1) ribs.push_back(temp);
			temp.clear();
			temp.push_back(graphPointsCountY * i + j);
			temp.push_back(graphPointsCountY * i + j + graphPointsCountY + 1);
			cout << "connecting " << graphPointsCountY * i + j << " with " << graphPointsCountY + j + graphPointsCountY + 1 << endl;
			temp.push_back(color);
			if ((rand() % 2) || !temp1 && !temp2) ribs.push_back(temp);
		}
	}
	for (int j = 0; j < graphPointsCountY - 1; ++j)
	{
		std::vector<int> temp;
		temp.clear();
		temp.push_back(graphPointsCountY * (graphPointsCountX - 1) + j);
		temp.push_back(graphPointsCountY * (graphPointsCountX - 1) + j + 1);
		temp.push_back(color);
		ribs.push_back(temp);
	}
}
void GetGraphMatrix(std::vector<NxVec3>& points, std::vector< std::vector<int> >& ribs) {
	std::vector<double> row;
	for (int i = 0; i < (int)points.size(); ++i) {
		row.clear();
		for (int j = 0; j < (int)points.size(); ++j) {
			row.push_back(0);
		}
		matrix.push_back(row);
	}
	for (int i = 0; i < (int)ribs.size(); ++i) {
		int p1 = (ribs[i])[0];
		int p2 = (ribs[i])[1];
		double x1, x2, y1, y2, z1, z2;
		x1 = points[p1].x;
		x2 = points[p2].x;
		y1 = points[p1].y;
		y2 = points[p2].y;
		z1 = points[p1].z;
		z2 = points[p2].z;
		(matrix[p1])[p2] = sqrt((x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1) + (z2 -
			z1) * (z2 - z1));
		(matrix[p2])[p1] = sqrt((x2 - x1) * (x2 - x1) + (y2 - y1) * (y2 - y1) + (z2 -
			z1) * (z2 - z1));
	}

}
int minElement(std::vector<float> labels, std::vector<bool> isVisits) {
	float minVal = 1e+6;
	float min = labels.size() + 1;
	for (int i = 0; i < (int)labels.size(); ++i) {
		if (!isVisits[i] && labels[i] < minVal) {
			minVal = labels[i];
			min = i;
		}
	}
	return min;
}
std::vector<int> deicstra(int start) {
	int N = matrix.size();
	std::vector<float> labels;
	std::vector<bool> isVisits;
	std::vector<int> path;
	for (int i = 0; i < N; ++i) {
		labels.push_back(1e+6);
		isVisits.push_back(false);
		path.push_back(start);
	}
	labels[start] = 0;
	std::priority_queue < float, std::vector<float>, std::greater<float> > vertexs;
	int indexVertex = start;
	do {
		for (int i = 0; i < N; ++i) {
			float h = (matrix[indexVertex])[i];
			if (h == 0) continue;
			if (h + labels[indexVertex] < labels[i]) {
				labels[i] = h + labels[indexVertex];
				path[i] = indexVertex;
			}
		}
		isVisits[indexVertex] = true;
		indexVertex = minElement(labels, isVisits);
	} while (indexVertex != labels.size() + 1);
	return path;
}
std::vector<int> path(int start, int end) {
	std::vector<int> paths = deicstra(start);
	std::vector<int> shortPath;
	int index = end;
	while (index != start) {
		shortPath.push_back(index);
		index = paths[index];
	}
	shortPath.push_back(start);
	return shortPath;
}
void painted(std::vector<int> path, int color) {
	for (int i = path.size() - 2; i >= 0; --i) {
		for (int j = 0; j < (int)ribs.size(); ++j) {
			if ((ribs[j])[0] == path[i] && (ribs[j])[1] == path[i + 1]
				|| (ribs[j])[1] == path[i] && (ribs[j])[0] == path[i + 1]) {
				(ribs[j])[2] = (ribs[j])[2] == 0 ? color : (ribs[j])[2] +
					color;
			}
		}
	}
}
int main(int argc, char** argv) {
	std::ofstream fout("C:\\Users\\mikhail\\Desktop\\graph.csv",std::ofstream::app);
	fout << "\"x\", \"y\", \"value\"" << std::endl;
	fout.close();
	GenerateGraph(points, ribs, graphPointsCountX, graphPointsCountY);
	GetGraphMatrix(points, ribs);
	PrintControls();
	InitGlut(argc, argv);
	InitNx();
	glutMainLoop();
	ReleaseNx();
	return 0;
}